#! /usr/bin/env python3

import os
import sys

import lib.plotting as plt
import lib.parse_statistics as parse

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

    # extract entropies from interval stat files
    data = parser.extract_entropies()
    data_norm = parser.extract_entropies(normalized=True)
    data_novel = parser.extract_entropies(novel=True)
    data_novel_norm = parser.extract_entropies(normalized=True, novel=True)
    data_cum = parser.extract_entropies(cumulative=True)

    # plot statistics
    result = plt.plot_bars(data, plot_name="Average Interval Entropy")
    result = result and plt.plot_bars(data_norm, plot_name="Average Normalized Interval Entropy")
    result = result and plt.plot_bars(data_novel, plot_name="Average Novelty Interval Entropy")
    result = result and plt.plot_bars(data_novel_norm, plot_name="Average Normalized Novelty Interval Entropy")
    result = result and plt.plot_bars(data_cum, plot_name="Average Cumulative Interval Entropy")

    # extract interval statistics by attribute
    data = parser.extract_by_attribute()

    if not result:
        return 1

    return 0

if __name__ == '__main__':
    main(sys.argv[1:])
