import csv
import os
import xml.etree.ElementTree as etree


class statistics_parser(object):

    def __init__(self, file_paths: list([str])):
        """
        

        :param file_paths: list with file paths
        """
        self.file_paths = file_paths
        self.label_files = {}
        self.interval_stats = {}
        self.interval_attributes = []
        self.parse_interval_stats_files()
        self.parse_labels()

    def parse_interval_stats_files(self):
        """
        
        """
        for file_path in self.file_paths:
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
                        data = list(data)[0]
                        for i, elem in enumerate(data):
                            data[i] = float(elem)
                        interval_stats.update({name: data})

            if not integrity:
                print("not an interval statistics file")

            return interval_stats

    def parse_labels(self):
        for file_path in self.file_paths:
            name = file_path[file_path.rfind("/")+1:-len(".interval_stat")]
            file_path = file_path[:-len(".interval_stat")]+"_labels.xml"
            if os.path.isfile(file_path):
                self.label_files.update({name: etree.parse(file_path).getroot()})

    def get_label_file(self, name: str):
        if name not in self.label_files.keys():
            return None
        return self.label_files[name]

    def get_label_file_info(self, name: str, label: str):
        if name not in self.label_files.keys():
            return None
        result = []
        for elem in self.label_files[name].iter():
            if elem.tag == label:
                result.append(elem.text)
        return result

    def get_label_files_info(self, label: str):
        label_files_info = {}
        for file_path in self.file_paths:
            name = file_path[file_path.rfind("/")+1:-len(".interval_stat")]
            label_files_info.update({name: self.get_label_file_info(name, label)})
        return label_files_info

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

    def extract_by_attribute(self):
        data = {}
        for attr in self.interval_attributes:
            data[attr] = self.extract_attribute(attr)
        return data

    def extract_attribute(self, attribute: str):
        """
        extracts the interval statistics values of a specific attribute.

        :param attribute: the attribute for which to get the interval statistics
        :return:
        """
        data = {}

        for name in self.interval_stats.keys():
            if attribute in self.interval_stats[name].keys():
                data.update({name: self.interval_stats[name][attribute]})

        return data
