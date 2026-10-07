import pytest
from models.search_result import SearchResult
from services.converter import convert_results


def test_convert_results_returns_search_results():
    raw = {"results": [
        {"id": 1, "media_type": "movie", "title": "A"},
        {"id": 2, "media_type": "tv", "name": "B"},
    ]}
    results = convert_results(raw)
    assert len(results) == 2
    assert all(isinstance(r, SearchResult) for r in results)
    assert [r.title for r in results] == ["A", "B"]


@pytest.mark.parametrize("raw", [None, {}, {"results": []}])
def test_convert_results_empty_or_missing_returns_empty_list(raw):
    assert convert_results(raw) == []