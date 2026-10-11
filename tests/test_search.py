from signalforge.search import SearchResult, search_web


def test_search_maps_ddgs_result(monkeypatch):
    class FakeDDGS:
        def text(self, query, max_results):
            return [{"title": "Example", "href": "https://example.org", "body": "Snippet"}]

    monkeypatch.setattr("signalforge.search.DDGS", FakeDDGS)
    assert search_web("example", 1) == [SearchResult("Example", "https://example.org", "Snippet")]


def test_blank_query_skips_provider(monkeypatch):
    monkeypatch.setattr("signalforge.search.DDGS", lambda: (_ for _ in ()).throw(AssertionError()))
    assert search_web("  ") == []


def test_search_filters_results_missing_requested_version(monkeypatch):
    class FakeDDGS:
        def text(self, query, max_results):
            return [
                {"title": "Python 3.12.10 release", "href": "https://good.example", "body": "3.12.10"},
                {"title": "Python 3.12.15 release", "href": "https://bad.example", "body": "3.12.15"},
            ]

    monkeypatch.setattr("signalforge.search.DDGS", FakeDDGS)
    results = search_web("Python 3.12.10 release", 2)
    assert [result.url for result in results] == ["https://good.example"]
