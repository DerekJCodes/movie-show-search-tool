from flask import Flask, request
from services.converter import convert_results

def create_app(client=None):
    app = Flask(__name__)

    @app.route("/search")
    def search():
        query = request.args.get("q", "")
        raw = client.search_multi(query)
        results = convert_results(raw)
        titles = [r.title for r in results]
        return "\n".join(titles)
    return app