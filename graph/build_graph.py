import json
import os
import pickle
from os.path import isfile, join
import graph


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

		cnt = 0
		for h in d[f][0]['href_list']:
			res = dir_of_file.get(str(h), None)
			cnt += int(res is not None)
		if cnt > 0 and len(d[f][0]['href_list']) == cnt:
			v.append(f)
			print (f, cnt)
	return v

def pr():
	in_deg = {}
	g = None
	with open('graph.bin', 'rb') as data:
		g = pickle.load(data)
	for v in g.vertex_list():
		if in_deg.get(v, -1) == -1:
			in_deg[v] = 0
		for u in g.adj_list(v):
			deg = in_deg.get(u, 0)
			in_deg[u] = deg + 1
	with open('pr.bin', 'wb') as pr_data:
		pickle.dump(in_deg, pr_data)

	print (in_deg[1741883])

def check_pr():
	with open('pr.bin', 'rb') as pr_data:
		in_deg = pickle.load(pr_data)
		print (in_deg[1741883])

def check_transform():
	g = None
	in_deg = None
	with open('graph.bin', 'rb') as data:
		g = pickle.load(data)
	with open('pr.bin', 'rb') as pr_data:
		in_deg = pickle.load(pr_data)
	for v in g.vertex_list():
		if in_deg[v] != g.in_degree(v):
			return False
	return True

if __name__ == '__main__':
    # build('records', 'records2')
	# vertices_with_neigbours('/home/austud/Documents/EDU/IR/arXiv/crawler/records')
	# pr()
	# check_pr()
	# transform()
	print (check_transform())
	
