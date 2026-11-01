from flask import Flask, render_template, request
from services.converter import convert_results
from services.tmdb_client import TMDBClient


def create_app(client=None):
    if client is None:
        client = TMDBClient()
    app = Flask(__name__)

    @app.route("/")
    def landing_page():
        return render_template("landing_page.html")

    @app.route("/search")
    def search():
        query = request.args.get("q", "")
        raw = client.search_multi(query)
        results = convert_results(raw)
        return render_template("search.html", query=query, results=results)

    return app