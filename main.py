#Imports go here
import sys

from services.exceptions import TMDBError
from services.tmdb_client import TMDBClient
from cli import run_search, friendly_error


def main(argv=None, client=None):
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

    print("Usage: python main.py search <query>")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
