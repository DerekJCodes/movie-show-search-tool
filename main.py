#Imports go here
from services.tmdb_client import search_multi
from services.converter import convert_results

def main():
    raw = search_multi("breaking-bad")
    results = convert_results(raw)
    for r in results[:5]:
        print(r.media_type, r.id, r.vote_average)

if __name__ == "__main__":
    main()
