# -*- coding: UTF-8 -*-
import xml.etree.ElementTree
from abc import ABCMeta, abstractmethod
import json
import requests
import os

ELASTIC_SEARCH_URL = "http://localhost:9200/"
ARXIV_DATA_DIR = "../data/"


# represents iterator over XML file
# Iterator should yield JSON structures
class XMLIterator:
    __metaclass__ = ABCMeta

    # Function iterate
    @abstractmethod
    def __iter__(self):
        pass


class ArxivXMLIterator(XMLIterator):
    # String - filename
    def __init__(self, filename):
        ArxivXMLIterator.cleanArxivXML(filename)
        self.xml = xml.etree.ElementTree.parse(filename).getroot()

    def __iter__(self):
        for x in self.xml[2]:
            json_data = {}
            try:
                json_data['arxivId'] = x[0][0].text
                json_data['authors'] = [t[0].text + " " + t[1].text for t in x[1][0].iter('author')]
                json_data['date'] = [t for t in x[1][0].iter('created')][0].text
                json_data['category'] = x[0][2].text
                json_data['caption'] = [t for t in x[1][0].iter('title')][0].text
                json_data['abstract'] = [t for t in x[1][0].iter('abstract')][0].text
            except IndexError:
                print("element was ignored\n")

            yield json.dumps(json_data)

    @staticmethod
    def cleanArxivXML(filename):
        with open(filename) as inp:
            lines = inp.readlines()
        inp.close()
        clean = []
        stop_words = ["ns0:", "ns2:"]
        for line in lines:
            tmp = line
            for word in stop_words:
                tmp = tmp.replace(word, "")
            clean.append(tmp)
        with open(filename, 'w') as otp:
            for line in clean:
                otp.write(line)
        otp.close()


if __name__ == '__main__':
    INDEX_URL = ELASTIC_SEARCH_URL + "arxiv/"
    id = 1
    for dirName, subdirList, fileList in os.walk(ARXIV_DATA_DIR):
        print('Found directory: %s' % dirName)
        for fname in fileList:
            filename = os.path.join(dirName, fname)
            print("parsing file {}".format(filename))
            for element in ArxivXMLIterator(filename):
                requests.put(INDEX_URL + "articles/{}".format(id), data=element)
                id += 1

    print("finished updating")
