#!/usr/bin/env python3

from flask import Flask, render_template, request, make_response
from Search import *
from settings import *
from utils import *
from suggestions import get_suggest

app = Flask(__name__)
agent = Search()
graph = load_graph(GRAPH_PATH)


@app.route("/")
def index():
    query = request.args.get('query')
    search_results = []
    if query is not None and len(query) > 0:
        search_results = agent.request(query)

    search_results = strip_element(search_results, "abstract", POST_MAX_LENGTH)
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

    references = graph.adj_list(paper_id)
    papers = []
    if len(references) > 0:
        papers = agent.references(references)

    history = []
    if request.cookies.get('history') is not None:
        history = request.cookies.get('history').split(",")
    if str(paper_id) not in history:
        history.append(str(paper_id))

    path = get_suggest(graph, paper_id, 10)
    history_papers, suggestion_papers = strip_element(agent.references(history), "title",
                                                      LEFT_BLOCK_LENGTH), strip_element(agent.references(path), "title",
                                                                                        LEFT_BLOCK_LENGTH)
    response = make_response(
        render_template("index.html", search_results=papers, history=history_papers, suggestion=suggestion_papers))
    response.set_cookie('history', ",".join(history))
    return response


if __name__ == "__main__":
    app.run("0.0.0.0", 8080)
