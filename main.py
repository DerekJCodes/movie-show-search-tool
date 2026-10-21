#Imports go here
import sys

from services.exceptions import TMDBError
from services.tmdb_client import TMDBClient
from cli import run_search, friendly_error, run_details


def main(argv=None, client=None, media_type=None, tmdb_id=None):
    if argv is None:
        argv = sys.argv[1:]
    client = client or TMDBClient()

    if len(argv) >= 2 and argv[0] == "search":
        query = " ".join(argv[1:])
        try:
            print(run_search(client, query))
        except TMDBError as exc:
            print(friendly_error(exc), file = sys.stderr)
            return 1
        return 0

    if len(argv) >= 3 and argv[0] == "details" and argv[1] in ("movie", "tv"):
        media_type = argv[1]

        try:
            tmdb_id = int(argv[2])
        except ValueError:
            print("The id must be a number, like: python main.py details movie 557", file=sys.stderr)
            return 1

        try:
            print(run_details(client, media_type, tmdb_id))
        except TMDBError as exc:
            print(friendly_error(exc), file=sys.stderr)
            return 1

        return 0
    USAGE = (
        "Usage:\n"
        "  python main.py search <query>\n"
        "  python main.py details <movie|tv> <id>"
    )
    print(USAGE, file = sys.stderr)
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
