import json
import os
import pickle
from os.path import isfile, join
from graph import *


def build(*dirs):
    files = []
    dir_of_file = {}
    for d in dirs:
        for f in os.listdir(d):
            if isfile(join(d, f)):
                files.append(f)
                dir_of_file[f] = d

    files = set(files)

    g = Graph()

    for f in files:
        with open(dir_of_file[f] + '/' + f) as data_file:
            data = json.load(data_file)
            for h in data[f][0]['href_list']:
                g.add_edge(int(f), int(h))

    with open('graph.bin', "wb") as data:
        pickle.dump(g, data)

    ts = TopSort()
    order = ts.sort(g)

    with open('order.bin', "wb") as data:
        pickle.dump(order, data)

if __name__ == '__main__':
    build('records', 'records2')
