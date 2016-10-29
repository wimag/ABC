import pickle
import graph

def load_graph(path):
    with open(path, 'rb') as raw_data:
        graph = pickle.load(raw_data)

    return graph
# class GraphAPI():
#
#     def __init__(self, path):
#         with open(path, 'rb') as raw_data:
#             self.graph = pickle.load(raw_data)
#
#     def get_references(self, id):
#         return self.graph.adj_list(id)
