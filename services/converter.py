from models.search_result import SearchResult

def convert_results(raw_json):
    """Turn the raw search/multi JSON into a list of SearchResult objects.

    Returns [] if there is no response body (the client returns None on a 404).
    """
    if not raw_json:
        return []
    return [SearchResult(item) for item in raw_json["results"]]