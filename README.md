# Movie & TV Show Search Tool

A Python-based search tool for movies and TV shows using a modular OOP architecture.  
API integration (TMDB/OMDb) will be added after the foundation is complete.

## Features (Planned)
- Search movies and shows
- Display formatted results
- Save items to a watchlist
- API integration
- Multithreaded search (future)

## Project Structure
- services/ — TMDB API client
- models/ — Movie, Show, SearchResult (planned)
- tests/ — pytest suite (initial test included)
- data/ — mock JSON for early testing (planned)
- main.py — entry point (planned)

## Development Notes
- Using movie ID `999999` during development to observe TMDB error behavior (401 with dummy key)
- More tests (404, 401, success cases) will be added later
- Additional endpoints (trending, popular, TV) planned

## Next Steps
This project will expand into:
- More pytest tests
- Additional TMDB endpoints
- Watchlist functionality
- Local data storage and formatting utilities

This repo serves as the backend foundation for a future movie/TV search tool.
