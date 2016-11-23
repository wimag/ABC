
class PageRank:
	pr = None

	def __init__(self, filename):
		self.pr = {}
		with open(filename) as data:
			lines = data.readlines()
			for l in lines:
				v, pr = l.split()
				self.pr[v] = pr

	def get_pagerank(self, v):
		return self.pr[v]
