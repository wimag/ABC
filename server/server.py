#!/usr/bin/env python3

from flask import Flask, render_template, request
app = Flask(__name__)

from Search import Search
from GraphAPI import GraphAPI
import settings

agent = Search()
graphApi = GraphAPI(settings.GRAPH_PATH)

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
    return render_template("index.html", search_results=search_results)

@app.route("/references")
def references():
    paper_id = request.args.get('id', '')

    try:
        paper_id = int(paper_id)
    except ValueError:
        peper_id = None

    if paper_id is None:
        return render_template("index.html", search_results=[])

    top_ids = [123]
    # search for tops
    references = agent.references(top_ids)
    if references is None:
        references = []

    return render_template("index.html", search_results=references)

if __name__ == "__main__":
    app.run()
