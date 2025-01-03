"""
Main.
"""

from pathlib import Path
import configparser

from utils.justwatch import check_watchlist
from utils.utils import get_ratings, open_watchlist, read_minimal_result


def main():
    """
    Main.
    """

    #   Opens config file
    config = configparser.ConfigParser()
    config_path = Path("config.ini")
    config.read(config_path)

    watchlist = open_watchlist()

    while True:
        print("\nOptions:")
        print("\t1. Check movie watchlist")
        print("\t2. View watchlist movies")
        print("\t2. Refresh ratings")

        choice = input("Choose an option (1/2/3): ")

        if choice == "1":
            check_watchlist(watchlist)
        elif choice == "2":
            read_minimal_result()
        elif choice == "3":
            get_ratings()

main()
