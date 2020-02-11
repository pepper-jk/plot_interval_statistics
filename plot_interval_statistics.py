#! /usr/bin/env python3

import csv
import os
import sys

import lib.plotting as plt


def parse_interval_stats(file_path: str) -> dict({str: list}):
    """
    Parsing function for ID2Ts interval statistics export files.

    :param file_path: path to input file
    :return: dictionary with statistics grouped by name
    """
    # open input file
    with open(file_path) as input_file:
        integrity = False
        interval_stats = {}

        # iterate over input file
        for line in input_file:
            # skip pcap file information
            if line.find("Interval statistics") != -1:
                integrity = True
            # read in interval stats
            if integrity:
                pos = line.find(":")
                # check syntax
                if pos != -1:
                    name = line[:pos]
                    # skip ':\t' at the beginning
                    data = csv.reader([line[pos+2:]], skipinitialspace=True)
                    interval_stats.update({name: list(data)[0]})

        if not integrity:
            print("not an interval statistics file")
        return interval_stats

def extract(file_paths: list([str]), normalized: bool=False, novel: bool=False, cumulative: bool=False)\
        -> list(dict({str: dict})):
    """
    Extract the entropies from interval statistics.

    :param file_paths: list with file paths
    :param normalized: extract normalized entropies
    :param novel: extract novelty entropies
    :param cumulative: extract cumulative entropies
    :return:
    """
    data = {}

    # iterate over all interval statistics file
    for file_path in file_paths:
        name = file_path[file_path.rfind("/")+1:-len(".interval_stat")]
        interval_stats = parse_interval_stats(file_path)

        # collect entropy entries
        entropy_keys = []
        for key in interval_stats.keys():
            if (key.find("entropy") != -1) and (not normalized or key.find("normalized") != -1) and \
                    (normalized or key.find("normalized") == -1) and (not novel or key.find("novel") != -1) and \
                    (novel or key.find("novel") == -1) and (not cumulative or key.find("cum") != -1) and \
                    (cumulative or key.find("cum") == -1):
                entropy_keys.append(key)

        # calculate entropy averages
        entropies = {}
        for key in entropy_keys:
            sum = 0
            for elem in interval_stats[key]:
                if elem == "None":
                    elem = 0
                sum += float(elem)
            average = round(sum / len(interval_stats[key]), 4)
            entropies.update({key[:key.find("_entropy")].replace("_novel", "").replace("_", " "): average})

        data.update({name: entropies})

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

    # extract entropies from interval stat files
    data = extract(file_paths)
    data_norm = extract(file_paths, normalized=True)
    data_novel = extract(file_paths, novel=True)
    data_novel_norm = extract(file_paths, normalized=True, novel=True)
    data_cum = extract(file_paths, cumulative=True)

    # plot statistics
    result = plt.plot_bars(data, plot_name="Average Interval Entropy")
    result = result and plt.plot_bars(data_norm, plot_name="Average Normalized Interval Entropy")
    result = result and plt.plot_bars(data_novel, plot_name="Average Novelty Interval Entropy")
    result = result and plt.plot_bars(data_novel_norm, plot_name="Average Normalized Novelty Interval Entropy")
    result = result and plt.plot_bars(data_cum, plot_name="Average Cumulative Interval Entropy")
    if not result:
        return 1

    return 0

if __name__ == '__main__':
    main(sys.argv[1:])
