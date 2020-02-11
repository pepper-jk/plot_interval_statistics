import csv


class statistics_parser(object):

    def __init__(self, file_paths: list([str])):
        """
        

        :param file_paths: list with file paths
        """
        self.file_paths = file_paths
        self.interval_stats = {}
        self.interval_attributes = []
        self.parse_interval_stats_files(self.file_paths)

    def parse_interval_stats_files(self, file_paths):
        """
        

        :param file_paths: list with file paths
        """
        for file_path in file_paths:
            name = file_path[file_path.rfind("/")+1:-len(".interval_stat")]
            interval_stats = self.parse_interval_stats(file_path)
            self.interval_stats[name] = interval_stats
        for attr in interval_stats.keys():
            self.interval_attributes.append(attr)
        self.interval_attributes = set(self.interval_attributes)

    def parse_interval_stats(self, file_path: str) -> dict({str: list}):
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

    def get_interval_attributes(self):
        return self.interval_attributes

    def get_interval_stats(self):
        return self.interval_stats

    def extract_entropies(self, normalized: bool=False, novel: bool=False, cumulative: bool=False)\
        -> list(dict({str: dict})):
        """
        Extract the entropies from interval statistics.

        :param normalized: extract normalized entropies
        :param novel: extract novelty entropies
        :param cumulative: extract cumulative entropies
        :return:
        """
        data = {}

        # iterate over all interval statistics file
        for name in self.interval_stats.keys():

            # collect entropy entries
            entropy_keys = []
            for key in self.interval_stats[name].keys():
                if (key.find("entropy") != -1) and (not normalized or key.find("normalized") != -1) and \
                        (normalized or key.find("normalized") == -1) and (not novel or key.find("novel") != -1) and \
                        (novel or key.find("novel") == -1) and (not cumulative or key.find("cum") != -1) and \
                        (cumulative or key.find("cum") == -1):
                    entropy_keys.append(key)

            # calculate entropy averages
            entropies = {}
            for key in entropy_keys:
                sum = 0
                for elem in self.interval_stats[name][key]:
                    if elem == "None":
                        elem = 0
                    sum += float(elem)
                average = round(sum / len(self.interval_stats[name][key]), 4)
                entropies.update({key[:key.find("_entropy")].replace("_novel", "").replace("_", " "): average})

            data.update({name: entropies})

        return data
