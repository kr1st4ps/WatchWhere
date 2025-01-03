"""
Other simple functions.
"""

import csv
import json

import requests


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


def get_ratings():
    """
    Collects ratings for all movies.
    """
    
    file_path = "data/output.json"
    api_key = "aec888a0"
    movie_ratings = {}

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        data_cnt = len(data)
        for (idx, movie) in enumerate(data):
            imdb_id = movie["imdb_id"]
            url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={api_key}"
            response = requests.get(url)
            resp_json = response.json()

            imdb_rating = resp_json.get("imdbRating", None)
            if imdb_rating:
                try:
                    imdb_rating = float(imdb_rating)
                except:
                    imdb_rating = None
            rt_rating = None
            for obj in resp_json.get("Ratings", []):
                if obj["Source"] == "Rotten Tomatoes":
                    rt_rating = int(obj["Value"][:-1])

            movie_ratings[imdb_id] = {
                "imdb_rating": imdb_rating,
                "rt_rating": rt_rating,
            }

            print(f"{idx} / {data_cnt}")

        with open("data/ratings.json", "w", encoding="utf-8") as file:
            json.dump(movie_ratings, file, indent=4, ensure_ascii=False)
