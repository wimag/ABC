#!/usr/bin/env python3

from flask import Flask, render_template, request, make_response

app = Flask(__name__)

from Search import Search
from GraphTools import load_graph
import settings

agent = Search()
graphApi = load_graph(settings.GRAPH_PATH)


def get_random_path(id, count):
    result = []
    for i in range(count):
        next = graphApi.adj_list(id)
        if len(next) == 0: return result
        result.append(next[0])
        id = next[0]

    return result


def find_paper(id):
    next = graphApi.adj_list(id)
    if len(next) == 0: return []
    next = sorted(next, key=lambda x: graphApi.in_degree(x), reverse=True)
    for i in next:
        if len(graphApi.adj_list(i)) == 0: return i
    return next[0]


def get_suggest(id, count):
    result = []
    for i in range(count):
        paper = find_paper(id)
        if paper is None: return result
        result.append(paper)

    return result


def prepare_for_view(search_results):
    for item in search_results:
        if len(item['abstract']) < settings.POST_MAX_LENGTH:
            continue

        item['abstract'] = item['abstract'][:settings.POST_MAX_LENGTH] + "..."

    return search_results


def prepare_for_view_left_items(items):
    for item in items:
        if len(item['title']) < settings.LEFT_BLOCK_LENGTH:
            continue

        item['title'] = item['title'][:settings.LEFT_BLOCK_LENGTH] + "..."

    return items


@app.route("/")
def index():
    query = request.args.get('query')
    search_results = []
    if query is not None and len(query) > 0:
        search_results = agent.request(query)

    search_results = prepare_for_view(search_results)
    response = make_response(render_template("index.html", search_results=search_results, history=[], suggestion=[]))
    response.set_cookie('history', '', expires=0)
    return response


@app.route("/references")
def references():
    paper_id = request.args.get('id', '')

    try:
        paper_id = int(paper_id)
    except ValueError:
        paper_id = None

    if paper_id is None:
        return render_template("index.html", search_results=[], suggestion=[])

    references = graphApi.adj_list(paper_id)
    papers = []
    if len(references) > 0:
        papers = agent.references(references)

    history = []
    if request.cookies.get('history') is not None:
        history = request.cookies.get('history').split(",")

    if str(paper_id) not in history: history.append(str(paper_id))

    history_papers = prepare_for_view_left_items(agent.references(history))
    path = get_suggest(paper_id, 10)
    suggestion_papers = prepare_for_view_left_items(agent.references(path))
    response = make_response(render_template("index.html", search_results=papers, history=history_papers, suggestion=suggestion_papers))
    response.set_cookie('history', ",".join(history))
    return response


if __name__ == "__main__":
    app.run("0.0.0.0", 8080)
