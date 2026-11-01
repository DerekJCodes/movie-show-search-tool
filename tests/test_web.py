from app import create_app
from models.tv_show import TVShow

class FakeWebClient:
    def search_multi(self, query):
        return {"results": [
            {"id": 1, "media_type": "movie", "title": "Alpha Movie",
             "release_date": "2002-05-01", "vote_average": 7.4},
            {"id": 2, "media_type": "tv", "name": "Beta Show",
             "first_air_date": "1994-11-19", "vote_average": 8.3},
            {"id": 3, "media_type": "person", "name": "Gamma Person"},
        ]}

class FakeTVClient:
    def get_tv_details(self, tv_id):
        return TVShow(id=tv_id, name="Breaking Bad", first_air_date="2008-01-20",
                      vote_average=9.0, overview="A teacher turns to crime.",
                      poster_path=None, number_of_seasons=5, number_of_episodes=62)


def test_search_page_lists_results():
    app = create_app(client=FakeWebClient())

    response = app.test_client().get("/search?q=spiderman")

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Alpha Movie" in body
    assert "Beta Show" in body

def test_search_page_links_movies_and_tv_but_not_people():
    app = create_app(client=FakeWebClient())

    body = app.test_client().get("/search?q=zzz").get_data(as_text=True)

    assert "/details/movie/1" in body
    assert "/details/tv/2" in body
    assert "Gamma Person" in body
    assert "/details/person" not in body