
class Graph:
	in_deg = None
	adj = None
	vertex = None
	directed = None

	def __init__(self, directed=True):
		self.adj = {}
		self.vertex = set()
		self.directed = directed
		self.in_deg = {}

	def add_vertex(self, v):
		self.vertex.add(v)
		self.check(v)

	def add_edge(self, v, u):
		self.vertex.add(v)
		self.vertex.add(u)
		self.check(v)
		self.check(u)

		self.adj[v].append(u)
		deg = self.in_deg.get(u, 0)
		self.in_deg[u] = deg + 1

		if not self.directed:
			self.adj[u].append(v)
			deg = self.in_deg.get(v, 0)
			self.in_deg[v] = deg + 1

	def in_degree(self, v):
		return self.in_deg.get(v, 0)

	def adj_list(self, v):
		return self.adj.get(v, None)

	def is_edge(self, v, u):
		f = u in self.adj_list(v)
		if not self.directed:
			f = f and (v in self.adj_list(u))
		return f

	def vertex_list(self):
		return [v for v in self.vertex]

	def check(self, v):
		if self.adj.get(v, None) is None:
			self.adj[v] = []


class TopSort:
    order = []
    used = {}

    def __init__(self):
        pass

    def sort(self, g):
        self.order = []
        self.used = {}

        for v in g.vertex_list():
            self.used[v] = False

        for v in g.vertex_list():
            if not self.used[v]:
                self.dfs(g, v)

        return self.order[::-1]

    def dfs(self, g, v):
        self.used[v] = True

        for u in g.adj_list(v):
            if not self.used[u]:
                self.dfs(g, u)

        self.order.append(v)
