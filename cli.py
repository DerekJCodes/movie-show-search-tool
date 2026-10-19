from services.exceptions import TMDBRateLimitError, TMDBAuthError, TMDBServerError, TMDBConnectionError

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