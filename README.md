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
- models/ — Movie, Show, SearchResult classes
- services/ — API client + formatting utilities
- data/ — mock JSON data for early testing
- watchlist/ — save/load watchlist items
- main.py — entry point