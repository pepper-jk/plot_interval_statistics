#! /usr/bin/env python3

import os
import sys

import lib.plotting as plt
import lib.parse_statistics as parse

def add_cumulative(attr: str, data):

    new_attr = attr+"_cumulative"
    data[new_attr] = {}
    for dataset, values in data[attr].items():
        next = 0.0
        cumulative = []
        for elem in values:
            next += float(elem)
            cumulative.append(next)
        data[new_attr].update({dataset:cumulative})

    return data

def main(argv):
    """
    Parsing, calculating and plotting average entropies from ID2T interval statistics files.

    :param argv: CLI arguments
    :return: 0 on success and error code on failure
    """
    # parse CLI arguments
    if len(argv) > 0:
        file_paths = []
        if os.path.isfile(argv[0]):
            file_paths = argv
        elif os.path.isdir(argv[0]):
            if argv[0][-1] != "/":
                argv[0] += "/"
            for file_name in os.listdir(argv[0]):
                file_paths.append(argv[0] + file_name)
        else:
            print("No such file or directory")
            return 2
    else:
        print("usage:")
        print("plot_interval_statistics.py <path_to_dir_containing_interval_stat_files>")
        print("plot_interval_statistics.py <path_to_file_containing_interval_stats> ...")
        return 1

    parser = parse.statistics_parser(file_paths)

    # extract interval statistics by attribute
    data = parser.extract_by_attribute()

    # 'correct_tcp_checksum_count', 'first_pkt_timestamp', 'incorrect_tcp_checksum_count', 'interval_count', 'ip_dst_cum_entropy',
    # 'ip_dst_cum_entropy_normalized', 'ip_dst_entropy', 'ip_dst_entropy_normalized', 'ip_dst_novel_count', 'ip_dst_novel_entropy',
    # 'ip_dst_novel_entropy_normalized', 'ip_src_cum_entropy', 'ip_src_cum_entropy_normalized', 'ip_src_entropy', 'ip_src_entropy_normalized',
    # 'ip_src_novel_count', 'ip_src_novel_entropy', 'ip_src_novel_entropy_normalized', 'kbyte_rate', 'kbytes', 'last_pkt_timestamp',
    # 'mss_entropy', 'mss_entropy_normalized', 'mss_novel_count', 'mss_novel_entropy', 'mss_novel_entropy_normalized', 'payload_count',
    # 'pkt_rate', 'pkts_count', 'port_entropy', 'port_entropy_normalized', 'port_novel_count', 'port_novel_entropy',
    # 'port_novel_entropy_normalized', 'tos_entropy', 'tos_entropy_normalized', 'tos_novel_count', 'tos_novel_entropy',
    # 'tos_novel_entropy_normalized', 'ttl_entropy', 'ttl_entropy_normalized', 'ttl_novel_count', 'ttl_novel_entropy',
    # 'ttl_novel_entropy_normalized', 'win_size_entropy', 'win_size_entropy_normalized', 'win_size_novel_count', 'win_size_novel_entropy',
    # 'win_size_novel_entropy_normalized'

    atk_timestamps = parser.get_label_files_info("timestamp")

    limiting_ts = []
    for timestamps in atk_timestamps.values():
        if timestamps != None:
            for ts in timestamps:
                limiting_ts.append(int(float(ts)*1000000))
            break

    limiting_ts.sort()
    limit = []
    previous_ts = limiting_ts[0]

    for val in data["last_pkt_timestamp"].values():
        for i, ts in enumerate(val):
            if int(ts) > limiting_ts[0] and len(limit) == 0:
                limiting_ts[0] = previous_ts
                limit.append(i+1)
            if int(ts) > limiting_ts[1] and len(limit) < 2:
                limiting_ts[1] = ts
                limit.append(i+1)
            previous_ts = ts
        break

    data = add_cumulative("ttl_entropy", data)

    attributes = {"pkt_rate": "Packets per Second",
                  # for attack only plot (instead of cumulative)
                  #"ttl_entropy": "TTL entropy",
                  "ttl_entropy_cumulative": "TTL Cumulative Entropy",
                  "ip_src_entropy": "IP Src. Entropy",
                  "ip_dst_entropy": "IP Dst. Entropy"}

    dataset_name = file_paths[0][:file_paths[0].rfind('/')]
    dataset_name = dataset_name[dataset_name.rfind('/')+1:]
    result = plt.plot_multi_lines(data, attributes, plot_name=dataset_name, vline=limit)

    if not result:
        return 1

    return 0

if __name__ == '__main__':
    main(sys.argv[1:])
