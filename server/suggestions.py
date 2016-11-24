from similarity import similarity_finder
from pagerank import *

pr = PageRank('../graph/PR_iter/4')


def get_random_path(graph, id, count):
    result = []
    for i in range(count):
        next = graph.adj_list(id)
        if len(next) == 0: return result
        result.append(next[0])
        id = next[0]

    return result


def normalize(f, min, max):
    if (min == max):
        return lambda x: 0

    return lambda x: (f(x) - min) / (max - min)


def find_paper(graph, id, query=None):
    from server import agent

    next = graph.adj_list(id)
    if len(next) == 0:
        return None

    if query is None:
        rank_algorithm = lambda x: graph.in_degree(x)
    else:
        text = lambda x: x['abstract'] if x['abstract'] else x['title']
        docs = {int(x['id']): text(x) for x in agent.papers(next)}
        similarity = lambda x: similarity_finder(query, docs[x]) if x in docs else 0
        min_similarity = min(map(similarity, next))
        max_similatity = max(map(similarity, next))

        page_rank = lambda x: pr.get_pagerank(x)
        min_pr = min(map(page_rank, next))
        max_pr = max(map(page_rank, next))

        rank_algorithm = lambda x: (normalize(similarity, min_similarity, max_similatity)(x) + normalize(page_rank,
                                                                                                         min_pr,
                                                                                                         max_pr)(x)) / 2
    next = sorted(next, key=rank_algorithm, reverse=True)
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

    return list(set(result))
