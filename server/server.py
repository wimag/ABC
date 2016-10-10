#!/usr/bin/env python3

from flask import Flask, render_template, request
app = Flask(__name__)

from Search import Search


empty = []
agent = Search()

@app.route("/")
def index():
    query = request.args.get('query')
    search_result = empty
    if query is not None and len(query) > 0:
        search_result = agent.request(query)
        print("Search for: {}".format(query))

    return render_template("index.html", search_results=search_result)

if __name__ == "__main__":
    app.run()
