"""
Turns client results and TMDB exceptions into text for the CLI. Nothing here prints,
so main.py owns output and exit codes and these functions stay easy to test.
"""
from services.exceptions import TMDBRateLimitError, TMDBAuthError, TMDBServerError, TMDBConnectionError
from services.converter import convert_results

def friendly_error(exc):
    """Turn a TMDB error exception into a one-line message for the user.

    Re-raises anything it doesn't recognize, so real bugs aren't hidden
    behind a friendly message.
    """
    if isinstance(exc, TMDBRateLimitError):
        #Explicit checks, not `if exc.retry_after:` because 0 is a real value
        #("try again now") and must not be treated like None ("unknown wait").
        if exc.retry_after == 0:
            return "Too many requests. You can try again now."
        if exc.retry_after is not None:
            return f"Too many requests. Try again in {exc.retry_after} seconds."
        return "Too many requests. Please wait a moment and try again."
    if isinstance(exc, TMDBAuthError):
        return "There's a problem with the API Key. Check TMDB_API_KEY in your .env file."
    if isinstance(exc, TMDBServerError):
        return "TMDB is having trouble right now. Try again later."
    if isinstance(exc, TMDBConnectionError):
        return "Couldn't reach TMDB. Check your internet connection."
    raise exc

#Maps TMDB's media_type values to display labels.
TYPE_LABELS = {"movie": "Movie", "tv": "TV", "person": "Person"}

def format_line(number, r):
    label = TYPE_LABELS[r.media_type]
    line = f"{number}. [{label}] {r.title}"
    #TMDB sends "" for an unknown date
    #Shows only the year; dates look like "YYYY-MM-DD".
    if r.date:
        line += f" ({r.date[:4]})"
    #People have no rating
    if r.media_type != "person":
        #TMDB sends 0 for "no votes yet", so 0 means N/A
        if r.vote_average:
            rating = f"{r.vote_average:.1f}"
        else:
            rating = "N/A"
        line += f" - Rating: {rating}"

    line += f" - id: {r.id}"

    return line

def format_results(results):
    """Format search results as numbered lines, or say none were found."""
    if not results:
        return "No results found."
    lines = []
    for number, r in enumerate(results, start=1):
        lines.append(format_line(number, r))
    return "\n".join(lines)

def run_search(client, query):
    """Search TMDB for a query and return the results as display text."""
    raw = client.search_multi(query)
    results = convert_results(raw)
    return format_results(results)

#Parameter is named other than credits solely to avoid shadowing Python's built-in object
def format_details(item, movie_credits):
    """Format a movie or TV show's details and top 5 cast as text."""
    if item.media_type == "tv":
        title, date = item.name, item.first_air_date
        info = (f"{item.number_of_seasons} {'season' if item.number_of_seasons == 1 else 'seasons'}, "
                f"{item.number_of_episodes} {'episode' if item.number_of_episodes == 1 else 'episodes'}")
    else:
        title, date = item.title, item.release_date
        runtime = f"{item.runtime} min" if item.runtime else "N/A"
        info = f"Runtime: {runtime}"

    year = f" ({date[:4]})" if date else ""
    rating = f"{item.vote_average:.1f}" if item.vote_average else "N/A"
    overview = item.overview or "No overview available."
    top_cast = ", ".join(member.name for member in movie_credits.cast[:5]) or "N/A"

    lines = [
        f"{title}{year}",
        f"Rating: {rating} | {info}",
        "",
        overview,
        "",
        f"Top cast: {top_cast}",
    ]
    return "\n".join(lines)

def run_details(client, media_type, tmdb_id):
    """
    Fetch a movie or TV show by TMDB id and return its details as text.

    Returns a "not found" message if the id doesn't exist.
    Raises ValueError if the media_type is not one of 'movie' or 'tv'.
    """
    if media_type == "tv":
        details = client.get_tv_details(tmdb_id)
        #Stored, not called yet: if the title doesn't exist we skip the
        #second API request entirely.
        get_credits = client.get_tv_credits
    elif media_type == "movie":
        details = client.get_movie_details(tmdb_id)
        get_credits = client.get_movie_credits
    else:
        #A wrong media_type is a programming mistake, so raise. (main.py
        #validates the user's input before calling this.)
        raise ValueError("media_type must be either 'movie' or 'tv'")
    # No need to raise an error as media details could be new and doesn't mean
    # it's invalid or so.
    if details is None:
        return f"No {media_type} found with id {tmdb_id}."
    return format_details(details, get_credits(tmdb_id))