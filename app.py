from flask import Flask, render_template, request
from services.converter import convert_results


def create_app(client=None):
    app = Flask(__name__)

    @app.route("/search")
    def search():
        query = request.args.get("q", "")
        raw = client.search_multi(query)
        results = convert_results(raw)
        return render_template("search.html", query=query, results=results)

    return app