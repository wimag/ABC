#!/usr/bin/env python3

from flask import Flask, render_template, request

app = Flask(__name__)

from Search import Search
from GraphTools import load_graph
import settings

agent = Search()
graphApi = load_graph(settings.GRAPH_PATH)


def prepare_for_view(search_results):
    for item in search_results:
        if len(item['abstract']) < settings.POST_MAX_LENGTH:
            continue

        item['abstract'] = item['abstract'][:settings.POST_MAX_LENGTH] + "..."

    return search_results


@app.route("/")
def index():
    query = request.args.get('query')
    search_results = []
    if query is not None and len(query) > 0:
        search_results = agent.request(query)

    search_results = prepare_for_view(search_results)
    print(search_results)
    return render_template("index.html", search_results=search_results)


@app.route("/references")
def references():
    paper_id = request.args.get('id', '')

    try:
        paper_id = int(paper_id)
    except ValueError:
        paper_id = None

    if paper_id is None:
        return render_template("index.html", search_results=[])

    references = graphApi.adj_list(paper_id)
    papers = []
    if len(references) > 0:
        papers = agent.references(references)

    return render_template("index.html", search_results=papers)


if __name__ == "__main__":
    app.run("0.0.0.0")
