#! /usr/bin/env python3

import sys

import lib.plotting as plt

# seconds it took to read statistics of a pcap
# get with:
# id2t -i <pcap> -ry -T     # regular
# id2t -i <pcap> -ry -t -T  # with extra tests
# num_pkts_mio is given by pcap, you need to provide pcaps with specific length manually
# then read seconds from output: Loaded file statistics in 159. sec by PCAP file processor.
# FORMAT: label: {num_pkts_mio: seconds}
read_statistics = {'Regular statistics': {'11': 193, '23': 392, '57': 1058, '212': 4033},
                   'With extra tests': {'11': 258, '23': 558, '57': 1354, '212': 5090}}

# seconds it took to generate a given amount of packets
# get with:
# id2t -i <pcap> -T -a DDoS attackers.count=10 packets.per-second=1000 bandwidth.max=100000
# num_pkts ~= attackers.count * packets.per-second
# read seconds from output: Generating attack packets... done. (total: 2000 pkts in 4.067694902420044 seconds.)
# FORMAT: attack: {num_pkts: seconds}
packets_generated = {'DDoS': {'10000': 15, '100000': 155, '1000000': 1231}}

def main(argv):
    """
    Plotting elapsed time from ID2T statistics calculations and packet generation.

    :param argv: CLI arguments
    :return: 0 on success and error code on failure
    """

    # plot statistics
    result = plt.plot(read_statistics, plot_name="read statistics", ylabel="Time (second)", xlabel="Number of packets (million)", annotate=True)
    result = result and plt.plot(packets_generated, plot_name="packets generated", ylabel="Time (second)", xlabel="Number of packets", annotate=True, legend=False)
    if not result:
        return 1

    return 0

if __name__ == '__main__':
    main(sys.argv[1:])
