from app import create_app
from models.movie import Movie
from models.tv_show import TVShow
from models.credits import Credits, CastMember

class FakeWebClient:
    def search_multi(self, query):
        return {"results": [
            {"id": 1, "media_type": "movie", "title": "Alpha Movie",
             "release_date": "2002-05-01", "vote_average": 7.4},
            {"id": 2, "media_type": "tv", "name": "Beta Show",
             "first_air_date": "1994-11-19", "vote_average": 8.3},
            {"id": 3, "media_type": "person", "name": "Gamma Person"},
        ]}

class FailingClient:
    def search_multi(self, query):
        raise AssertionError("home page must not call TMDB")

class FakeDetailsWebClient:
    def get_movie_details(self, movie_id):
        return Movie(id=movie_id, title="Gamma Film", release_date="2001-03-04",
                     vote_average=7.4, runtime=121,
                     overview="A distinctive overview.", poster_path=None)

    def get_movie_credits(self, movie_id):
        return Credits(cast=[CastMember(1, "Zed Actor", "Hero Role", None)], crew=[])

    def get_tv_details(self, tv_id):
        return TVShow(id=tv_id, name="Delta Series", first_air_date="2010-05-06",
                      vote_average=8.8, overview="Another distinctive overview.",
                      poster_path=None, number_of_seasons=1, number_of_episodes=16)

    def get_tv_credits(self, tv_id):
        return Credits(cast=[CastMember(2, "Yara Actress", "Lead Role", None)], crew=[])

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

def test_create_app_builds_the_real_client_by_default(monkeypatch):
    monkeypatch.setattr("app.TMDBClient", FakeWebClient)

    app = create_app()

    response = app.test_client().get("/search?q=zzz")
    assert response.status_code == 200
    assert "Alpha Movie" in response.get_data(as_text=True)

def test_home_page_shows_search_box_without_calling_tmdb():
    app = create_app(client=FailingClient())

    response = app.test_client().get("/")
    body = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'data-testid="search-input"' in response.get_data(as_text=True)
    assert "Find any movie or TV show" in body

def test_movie_details_page_shows_info_and_cast():
    app = create_app(client=FakeDetailsWebClient())

    response = app.test_client().get("/details/movie/557")

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Gamma Film" in body
    assert "2001" in body
    assert "121 min" in body
    assert "A distinctive overview." in body
    assert "Zed Actor" in body
    assert "Hero Role" in body


def test_tv_details_page_shows_seasons_and_cast():
    app = create_app(client=FakeDetailsWebClient())

    response = app.test_client().get("/details/tv/219246")

    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Delta Series" in body
    assert "1 season, 16 episodes" in body
    assert "Yara Actress" in body