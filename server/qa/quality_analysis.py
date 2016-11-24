from time import sleep

from selenium import webdriver
import re
import os
from difflib import SequenceMatcher

def similar(a, b):
    a = re.sub('[^0-9a-zA-Z]+', '', a).lower()
    b = re.sub('[^0-9a-zA-Z]+', '', b).lower()
    return SequenceMatcher(None, a, b).ratio()


class ScholarQualityAnalizer:

    def start(self):
        self.driver = webdriver.Chrome(executable_path="/home/wimag/Yandex.Disk/My Stuff/SPBAU/IR/ABC/server/qa/chromedriver")
        self.driver.get("http://www.google.com")
        url = "https://scholar.google.ru/scholar?q=test"
        self.driver.get(url)
        sleep(15)
    def close(self):
        self.driver.close()

    def compare_with_scholar(self, query, query_results):
        scholar_results = self.get_scholar_ordering(query)
        print(scholar_results)
        return sum([int(max(0, 0, *[similar(x['title'], t) for t in scholar_results]) > 0.7) for x in query_results]) / min(len(query_results), len(scholar_results))


    def get_scholar_ordering(self, query):
        query_words = [str(x) for x in re.sub('[^0-9a-zA-Z]+', ' ', query).lower().split() if x.isalpha()]
        words = "+".join(query_words)
        sleep(2)
        url = "https://scholar.google.ru/scholar?q=" + words
        self.driver.get(url)
        elements = self.driver.find_elements_by_class_name("gs_rt")
        results = [x.text for x in elements]
        return results

analyzer = ScholarQualityAnalizer()

if __name__ == "__main__":
    analyzer.start()
    print(analyzer.get_scholar_ordering("test"))