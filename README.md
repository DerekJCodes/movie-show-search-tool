# ReelFinder: A Movie & TV Show Search Tool

[![Tests](https://github.com/DerekJCodes/movie-show-search-tool/actions/workflows/tests.yml/badge.svg)](https://github.com/DerekJCodes/movie-show-search-tool/actions/workflows/tests.yml)

A Python-based movie and TV search tool built around the TMDB API using an object-oriented and test-driven architecture.

## Setup
- First steps - clone repo: 
  - `git clone https://github.com/DerekJCodes/movie-show-search-tool.git`
  - `cd movie-show-search-tool`
- Setup environment/requirements:
  - .venv (Virtual environment setup):
    - `python -m venv .venv`
    - Git Bash: `source .venv/Scripts/activate`
    - PowerShell(PS) / Command Prompt(CP): `.venv\Scripts\activate`
    - Mac/Linux: `source .venv/bin/activate`
  - `pip install -r requirements.txt`
  - .env with API key: `TMDB_API_KEY=your_key_here`
    - To get a TMDB API key:
      - Navigate to: https://www.themoviedb.org/
      - Login/Create Account
      - Navigate to Settings → API tab under profile picture
      - Generate API key via TMDB
      - Paste API key in .env at root of project

## Usage
- In main.py, there are two usage commands via CLI:
```
python main.py search <query>
python main.py details <movie/tv> <id>
```
- `<query>` is a string for what you want to search for 
- `<movie/tv>` either `movie` or `tv`, TMDB numbers movies and shows
separately, so the same ID can exist in both.
- `<id>` is an int value of TMDB's real media ID to match their respective
media data (title, rating, release date/first air date, etc.)
  - Ex. `python main.py search spiderman`
    ```
    $ python main.py search spiderman
    1. [Movie] Spider-Man: Brand New Day (2026) - Rating: 8.5 - id: 969681
    2. [Movie] Spider-Man (2002) - Rating: 7.4 - id: 557
    3. [TV] Spider-Man (1994) - Rating: 8.3 - id: 888
    ```
    - (Up to 20 results)
  - Ex. `python main.py details tv 219246`
    ```
    $ python main.py details tv 219246
    When Life Gives You Tangerines (2025)
    Rating: 8.8 | 1 season, 16 episodes

    In Jeju, a spirited girl and a steadfast boy's island story blossoms into a lifelong tale of setbacks and triumphs — proving love endures across time.

    Top cast: IU, Park Bo-gum, Moon So-ri, Park Hae-joon
    ```
    - Example output when searching for a TV show based on their TMDB ID
    - Returns:
      - Title 
      - Release Date
      - Rating
      - Season & Episode Count 
      - Description
      - Top Cast (Up to 5 Names)
- For logging purposes:
  - `LOG_LEVEL` sets how much is logged: `DEBUG`, `INFO` (default), `WARNING`, `ERROR`
  - `LOG_FILE` sets where it's written (default `reelfinder.log`)
    - Ex. (Git Bash or Mac/Linux) `LOG_LEVEL=DEBUG python main.py search spiderman`
      - PowerShell users set the variable first `$env:LOG_LEVEL="DEBUG"`, then
      run the command.

## Testing
- Unit test: `pytest`, these are what CI runs on every PR
- Integration test: `pytest -m integration` <i>Needs the key and a network connection</i>
- E2E test: `pytest -m e2e` <i>Needs the key and a network connection</i>
- With coverage: `pytest --cov`

## Current Features
- TMDB API client
- Multi-search support
- Movie details endpoint
- TV details endpoint
- Movie credits endpoint
- TV credits endpoint
- Movie model parsing
- TVShow model parsing
- Credits parsing
- PyTest coverage for validation and endpoint handling
- API trace logging
- Custom friendly error handling
- Unit, integration, and End-to-End (E2E) testing
- CLI search experience
- GitHub Actions CI running the unit tests on every PR

## Project Structure
- services/ — TMDB API client, parsers, & custom exceptions
- models/ — Movie, TVShow, Credits, SearchResult
- tests/ — PyTest suite
- main.py — CLI project entry point with search and details
- cli.py - output formatting
- logging_config.py - Log file and level setup
- .github/workflows/ - CI
- requirements.txt - pinned dependencies

## Next Steps
- Frontend structure development
- Additional TMDB endpoints
- Watchlist functionality
- Add Playwright E2E tests 
- Linting (black/flake8)

## Credits
<i>This product uses the TMDB API but is not endorsed or certified by TMDB.</i>
<img src="https://www.themoviedb.org/assets/v4/logos/v2/blue_long_2-9665a76b1ae401a510ec1e0ca40ddcb3b0cfe45f1d51b77a308fea0845885648.svg">