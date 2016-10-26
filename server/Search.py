from elasticsearch import Elasticsearch

from settings import HOST, PORT, INDEX


class Search(object):
    def __init__(self):
        self.connection = Elasticsearch([{'host': HOST, 'port': PORT}])
        pass

    def request(self, query):
        result = self.connection.search(index=INDEX, body={
            'query': {
                'match': {
                    'abstract': {
                        'query': query,
                        'type': 'phrase_prefix',
                        'max_expansions': 50
                    }
                }
            },
            'sort': ['_score']
        })

        response = result['hits']['hits']
        return list(map(lambda x: x['_source'], response))

    def references(self, ids):
        response = self.connection.mget(index=INDEX,
             doc_type='article',
             body={'ids': list(map(str, ids))})

        print(response)
        return None
