"""
Other simple functions.
"""

import csv
import json


def open_watchlist():
    """
    Opens watchlist
    """

    file_path = "data/watchlist.csv"

    watchlist = []

    with open(file_path, "r", newline="", encoding="utf-8") as csvfile:
        csv_reader = csv.DictReader(csvfile)

        for row in csv_reader:
            watchlist.append(row)

    return watchlist


def read_minimal_result():
    """
    Opens minimal result
    """

    file_path = "minimal_output.json"

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        valid_services = ["Go3", "Netflix", "Amazon Prime Video"]

        for entry in data:
            valid_results = []
            for offer in entry["offers"]:
                if offer["type"] == "STREAM" and offer["service"] in valid_services:
                    valid_results.append(offer["service"])

            if valid_results:
                print(entry["name"])
                for res in valid_results:
                    print(f"\t{res}")
                print()
