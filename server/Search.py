from elasticsearch import Elasticsearch

from settings import HOST, PORT, INDEX

fish = [{
    'href': 'http://127.0.0.1',
    'title': 'Data processing on CPU',
    'annotation': '''Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum'''
}]

class Search(object):
    def __init__(self):
        self.connecton = Elasticsearch([{'host': HOST, 'port': PORT}])
        pass

    def request(self, query):
        result = self.connecton.search(index=INDEX, body={"query": {"match": {'title': query}}})
        response = result['hits']['hits']
        return list(map(lambda x: x['_source'], response))

