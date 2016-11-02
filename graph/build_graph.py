import json
import os
import pickle
from os.path import isfile, join
from graph import *


def get_files(*dirs):
	files = []
	dir_of_file = {}
	for d in dirs:
		for f in os.listdir(d):
			if isfile(join(d, f)):
				files.append(f)
				dir_of_file[f] = d

	return (set(files), dir_of_file)

def build(*dirs):
    files, dir_of_file = get_files(*dirs)

    g = Graph()

    for f in files:
        with open(dir_of_file[f] + '/' + f) as data_file:
            d = json.load(data_file)

        for h in d[f][0]['href_list']:
            g.add_edge(int(f), int(h))

    with open('graph.bin', "wb") as datafile:
        pickle.dump(g, datafile)

    ts = TopSort()
    order = ts.sort(g)

    with open('order.bin', "wb") as data:
        pickle.dump(order, data)

def vertices_with_neigbours(*dirs):
	v = []
	files, dir_of_file = get_files(*dirs)
	for f in files:
		with open(dir_of_file[f] + '/' + f) as data_file:
			d = json.load(data_file)

		flag = True
		for h in d[f][0]['href_list']:
			res = dir_of_file.get(h, None)
			flag = flag and (res is not None)
		if flag:
			v.append(f)
			print (f)
	return v


if __name__ == '__main__':
    # build('records', 'records2')
	vertices_with_neigbours('/home/austud/Documents/EDU/IR/arXiv/crawler/records')
	
