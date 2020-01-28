#! /usr/bin/env python3

import sys

import lib.plotting as plt

read_statistics = {'Regular statistics': {'11': 193, '23': 392, '57': 1058, '212': 4033},
                   'With extra tests': {'11': 258, '23': 558, '57': 1354, '212': 5090}}
packets_generated = {'DDoS': {'10000': 15, '100000': 155, '1000000': 1231}}

def main(argv):
    """
    Plotting elapsed time from ID2T statistics calculations and packet generation.

    :param argv: CLI arguments
    :return: 0 on success and error code on failure
    """

    # plot statistics
    result = plt.plot(read_statistics, plot_name="read statistics", ylabel="Time (second)", xlabel="Number of packets (million)", annotate=True)
    result = result and plt.plot(packets_generated, plot_name="packets generated", ylabel="Time (second)", xlabel="Number of packets", annotate=True)
    if not result:
        return 1

    return 0

if __name__ == '__main__':
    main(sys.argv[1:])
