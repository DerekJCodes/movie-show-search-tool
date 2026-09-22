#Imports go here
from services.tmdb_client import search_multi
from services.converter import convert_results

def main():
    raw = search_multi("breaking-bad")
    results = convert_results(raw)
    for r in results[:5]:
        print(f"Type: {r.media_type.capitalize()}")
        print(f"Title:", getattr(r,"title", getattr(r,"name", None)))
        print(f"")

if __name__ == "__main__":
    main()
