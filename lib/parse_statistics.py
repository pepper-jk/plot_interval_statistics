import csv


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

def extract_entropies(file_paths: list([str]), normalized: bool=False, novel: bool=False, cumulative: bool=False)\
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