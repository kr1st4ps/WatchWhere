"""
Docstring
"""
import csv
from pathlib import Path
import configparser
from justwatch import JustWatch


def open_watchlist():
    """
    Opens watchlist
    """

    file_path = "watchlist.csv"

    watchlist = []

    with open(file_path, "r", newline="", encoding="utf-8") as csvfile:
        csv_reader = csv.DictReader(csvfile)

        for row in csv_reader:
            watchlist.append(row)

    return watchlist


def write_to_csv(data, file_path, headers=None):
    """
    Writes result
    """

    try:
        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)

            if headers:
                csv_writer.writerow(headers)

            for row in data:
                csv_writer.writerow(row)

    except Exception as e:
        print(f"Error occurred while writing to CSV file: {e}")


def main():
    """
    Main
    """

    #   Opens config file
    config = configparser.ConfigParser()
    config_path = Path("config.ini")
    config.read(config_path)

    watchlist = open_watchlist()

    while True:
        print("\nOptions:")
        print("1. Check streaming services")

        choice = input("Choose an option (1/...): ")

        if choice == "1":
            result = []
            for movie in watchlist:
                name = movie["Name"]

                result.append([name])

            write_to_csv(result, "result.csv")


main()
