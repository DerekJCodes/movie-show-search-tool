from services.exceptions import TMDBRateLimitError, TMDBAuthError, TMDBServerError, TMDBConnectionError
from services.converter import convert_results

def friendly_error(exc):
    if isinstance(exc, TMDBRateLimitError):
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

TYPE_LABELS = {"movie": "Movie", "tv": "TV", "person": "Person"}

def format_line(number, r):
    label = TYPE_LABELS[r.media_type]
    line = f"{number}. [{label}] {r.title}"

    if r.date:
        line += f" ({r.date[:4]})"

    if r.media_type != "person":
        if r.vote_average:
            rating = f"{r.vote_average:.1f}"
        else:
            rating = "N/A"
        line += f" - Rating: {rating}"

    line += f" - id: {r.id}"

    return line

def format_results(results):
    if not results:
        return "No results found."
    lines = []
    for number, r in enumerate(results, start=1):
        lines.append(format_line(number, r))
    return "\n".join(lines)

def run_search(client, query):
    raw = client.search_multi(query)
    results = convert_results(raw)
    return format_results(results)