from flask import Flask, render_template, request, abort
from services.converter import convert_results
from services.tmdb_client import TMDBClient

def _details_view(item, credits):
    """Turn a Movie or TVShow plus its credits into one shape for the template."""
    if item.media_type == "tv":
        title, date = item.name, item.first_air_date
        info = (f"{item.number_of_seasons} {'season' if item.number_of_seasons == 1 else 'seasons'}, "
                f"{item.number_of_episodes} {'episode' if item.number_of_episodes == 1 else 'episodes'}")
    else:
        title, date = item.title, item.release_date
        info = f"{item.runtime} min" if item.runtime else ""
    rating = f"★ {item.vote_average:.1f}" if item.vote_average else "No rating"
    meta = " · ".join(part for part in (date[:4] if date else "", rating, info) if part)
    return {
        "title": title,
        "meta": meta,
        "overview": item.overview or "No overview available.",
        "poster_path": item.poster_path,
        "media_type": item.media_type,
        "cast": credits.cast[:5] if credits else [],
    }

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

    @app.route("/details/<media_type>/<int:tmdb_id>")
    def details(media_type, tmdb_id):
        if media_type == "tv":
            item = client.get_tv_details(tmdb_id)
            get_credits = client.get_tv_credits
        elif media_type == "movie":
            item = client.get_movie_details(tmdb_id)
            get_credits = client.get_movie_credits
        else:
            abort(404)
        if item is None:
            abort(404)
        return render_template("details.html", d=_details_view(item, get_credits(tmdb_id)))

    return app