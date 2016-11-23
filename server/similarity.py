from gensim.models import Doc2Vec
import re


class SimilarityFinder:
    def __init__(self):
        self.model = Doc2Vec.load('../data/sims.bin')

    def find_semantic_similarity(self, query, doc):
        if type(query) is str:
            query_words = [x for x in re.sub('[^0-9a-zA-Z]+', ' ', query).lower().split() if x.isalpha()]
        else:
            query_words = query
        if type(doc) is str:
            doc_words = [x for x in re.sub('[^0-9a-zA-Z]+', ' ', doc).lower().split() if x.isalpha()]
        else:
            doc_words = doc

        filtered_query = [x for x in query_words if x in self.model.vocab]
        filtered_doc = [x for x in doc_words if x in self.model.vocab]

        if not filtered_query or not filtered_doc:  # One of vectors is empty
            # return Jaccard similarity
            return len(set(query_words).intersection(set(doc_words))) / len(set(query_words + doc_words))
        else:
            # return vector similarity
            return self.model.n_similarity(filtered_query, filtered_doc)

    def __call__(self, query, doc):
        return self.find_semantic_similarity(query, doc)


similarity_finder = SimilarityFinder()
