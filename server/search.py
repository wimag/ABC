from elasticsearch import Elasticsearch

from settings import HOST, PORT, INDEX


class search(object):
    def __init__(self):
        self.connection = Elasticsearch([{'host': HOST, 'port': PORT}])
        pass

    def request(self, query):
        result = self.connection.search(index=INDEX, body={
            'query': {
                'match': {
                    'abstract': {
                        'query': query,
                        'operator': 'or'
                    }
                }
            },
            'sort': ['_score']
        })

        response = result['hits']['hits']
        return list(map(lambda x: x['_source'], response))

    def papers(self, ids):
        response = self.connection.mget(index=INDEX,
                                        doc_type='articles',
                                        body={'ids': ids})

        founded = lambda x: x['found']
        source = lambda x: x['_source']
        return list(map(source, filter(founded, response['docs'])))
