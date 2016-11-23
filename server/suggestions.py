from similarity import similarity_finder


def get_random_path(graph, id, count):
    result = []
    for i in range(count):
        next = graph.adj_list(id)
        if len(next) == 0: return result
        result.append(next[0])
        id = next[0]

    return result


def find_paper(graph, id, query=None):
    from server import agent

    next = graph.adj_list(id)
    if len(next) == 0:
        return None

    if query is None:
        similarity = lambda x: graph.in_degree(x)
    else:
        text = lambda x: x['abstract'] if x['abstract'] else x['title']
        docs = {int(x['id']): text(x) for x in agent.papers(next)}
        similarity = lambda x: similarity_finder(query, docs[x]) if x in docs else 0

    next = sorted(next, key=similarity, reverse=True)
    for i in next:
        if len(graph.adj_list(i)) != 0:
            return i

    return next[0]


def get_suggest(graph, id, count, query=None):
    result = []
    for i in range(count):
        paper = find_paper(graph, id, query=query)
        if paper is None: return result
        result.append(paper)
        id = paper

    return result
