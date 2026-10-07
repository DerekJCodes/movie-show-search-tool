from models.search_result import SearchResult

def convert_results(raw_json):
    if not raw_json:
        return []
    return [SearchResult(item) for item in raw_json["results"]]