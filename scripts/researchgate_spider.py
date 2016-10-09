import scrapy
import re
import json
import pickle
from os.path import isfile
from collections import deque


class ResearchGateSpider(scrapy.Spider):
    name = "researchgate"
    base = 'https://www.researchgate.net/'

    id = None
    title = None
    author_list = None
    abstract = None
    href_count = None
    citations_list = None

    visited = {}
    queue = deque()

    cookie = {
        'sid': 'KOrMAWaE75O2uvUsOHKknASs32EGwMdEqIFWG6bbkCIK6IU8QlQ1lAdcMxrH2Jy4neZ7E5NhNPvUL5xLt0TsumDosf7MIvMuzka1ocyIL82zMLJf7qKvHvPXls6jdD1U',
        'did': 'fJduQ4THQPEiJ0olJIdVdT0zaBl1T4irSU4NxP9YhfLF46k0zt3XdYtKo1UkHi3k',
        '__gads': 'ID=4a4ebd0519fdf249:T=1475927008:S=ALNI_MZa2nW_5bGfUyuxwIGYTXSUxxPcdA',
        'cookieHidePopup': 'vC6Wag0su0aYaCV1rdMXIgzv71l4gAUoBOsheZdNglKcIOFfkRREU827RzxpfdCZbz20YR8JdMse8sFI660xdGuINaToripc0WJcBWJ2wEkbvxfDdtAZN0773T3wil15',
        'ptc': 'RG1.4113912968274291316.1475927003',
        'captui': 'M2E5ZDI3YTdjN2ZmYTNiZDRjMWM4OGFkNDg5ODkxNzlkMmRkNDVlOTdhOGZkNzI4MmE5NTk5NTg4ZTVhNzQzNF9jU3FRUU9QRzF4djdTcEVFckZFNGJSaGVUUGY0akNjbnNFU3I%3D',
        '_ga': 'GA1.2.118311245.1475927007',
        '_gat': '1'
    }

    @staticmethod
    def serialize(obj, filename):
        with open(filename, "wb") as data:
            pickle.dump(obj, data)

    @staticmethod
    def deserialize(filename):
        with open(filename, "rb") as data:
            return pickle.load(data)

    def init(self):
        if isfile('visited'):
            self.visited = ResearchGateSpider.deserialize('visited')

        if isfile('queue'):
            self.queue = ResearchGateSpider.deserialize('queue')

        if len(self.queue) == 0:
            self.queue.append(285164623)

    def start_requests(self):
        self.init()
        url = self.queue.popleft()
        yield scrapy.Request(url=self.base + 'publication/' + str(url), callback=self.parse, cookies=self.cookie)

    def parse(self, response):
        if response.status != 200 and response.status != 301:
            exit(1)

        self.log(self.id)

        self.id = int(re.search('\d+', response.url).group(0))

        self.visited[self.id] = True

        self.title = ResearchGateSpider.get_title(response)
        self.author_list = ResearchGateSpider.get_author_list(response)
        self.abstract = ResearchGateSpider.get_abstract(response)
        self.href_count = ResearchGateSpider.get_citations_count(response)

        req_str = 'publicliterature.PublicPublicationReferenceList.loadPublicPublications.html?' \
                  'publicationUid=' + str(self.id) + '&offset=0&limit=' + str(self.href_count)

        yield scrapy.Request(url=self.base + req_str, callback=self.citations_list_parse, cookies=self.cookie)

    def citations_list_parse(self, response):
        data = json.loads(response.body_as_unicode())
        self.citations_list = [int(x) for x in data["result"]["publicliteraturePublicPublicationReferenceItems"]]

        record = {
            self.id: [
                {
                    'title': self.title,
                    'author_list': self.author_list,
                    'abstract': self.abstract,
                    'href_count': self.href_count,
                    'href_list': self.citations_list,
                }
            ]
        }

        with open('records/' + str(self.id), 'a') as f:
            json.dump(record, f)

        for c_id in self.citations_list:
            if self.visited.get(c_id) is None:
                self.visited[c_id] = True
                self.queue.append(c_id)

        ResearchGateSpider.serialize(self.queue, 'queue')
        ResearchGateSpider.serialize(self.visited, 'visited')

        if len(self.queue) > 0:
            i = self.queue.popleft()
            yield scrapy.Request(self.base + 'publication/' + str(i), self.parse, cookies=self.cookie)

    @staticmethod
    def get_citations_count(response):
        for tab in response.css('li.ReactTabs__Tab'):
            t = tab.css('span.title-tab-interaction::text').extract_first()
            if t == 'References':
                return tab.css('span.nova-e-badge::text').extract_first()
        return 0

    @staticmethod
    def get_abstract(response):
        abstract = response.css('div.publication-abstract')
        return abstract.css('div.nova-e-text::text').extract_first()

    @staticmethod
    def get_title(response):
        publication_header = response.css('div.publication-header')
        return publication_header.css('h1.publication-title::text').extract_first()

    @staticmethod
    def get_author_list(response):
        publication_header = response.css('div.publication-header')
        return [author.css('a.publication-author-name::text').extract_first()
                for author in publication_header.css('li.publication-author-list-item')]
