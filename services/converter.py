from models.search_result import SearchResult

def convert_results(raw_json):
    return [SearchResult(item) for item in raw_json["results"]]