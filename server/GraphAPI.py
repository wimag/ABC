import pickle

class GraphAPI():

    def __init__(self, path):
        with open(path, 'rb') as raw_data:
            self.graph = pickle.load(raw_data)

    def get_neighours(self, id):
        return self.graph.adj_list(id)
