def get_random_path(graph, id, count):
    result = []
    for i in range(count):
        next = graph.adj_list(id)
        if len(next) == 0: return result
        result.append(next[0])
        id = next[0]

    return result


def find_paper(graph, id):
    next = graph.adj_list(id)
    if len(next) == 0:
        return None

    next = sorted(next, key=lambda x: graph.in_degree(x), reverse=True)
    for i in next:
        if len(graph.adj_list(i)) != 0:
            return i

    return next[0]


def get_suggest(graph, id, count):
    result = []
    for i in range(count):
        paper = find_paper(graph, id)
        if paper is None: return result
        result.append(paper)
        id = paper

    return result
