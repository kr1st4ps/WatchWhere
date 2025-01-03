"""
Docstring
"""

import csv
from dataclasses import dataclass
import json
from pathlib import Path
import configparser
from simplejustwatchapi.justwatch import search, offers_for_countries

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

def read_minimal_result():
    """
    Opens minimal result
    """

    file_path = "minimal_output.json"

    with open(file_path, 'r', encoding='utf-8') as file:
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

@dataclass
class MediaObject:
    title: str
    year: int
    runtime: int
    url: str
    type: str
    description: str
    genres: list
    imdb_id: str
    poster_url: str
    offers: list

    def to_dict(self):
        """Convert the class instance to a dictionary."""
        return {
            "title": self.title,
            "year": self.year,
            "runtime": self.runtime,
            "url": self.url,
            "type": self.type,
            "description": self.description,
            "genres": self.genres,
            "imdb_id": self.imdb_id,
            "poster_url": self.poster_url,
            "offers": self.offers,
        }


@dataclass
class MediaOffer:
    type: str
    quality: str
    price: float
    currency: str
    service: str
    service_icon_url: str
    url: str
    subtitles: list
    audio: list

    def to_dict(self):
        """Convert the class instance to a dictionary."""
        return {
            "type": self.type,
            "quality": self.quality,
            "price": self.price,
            "currency": self.currency,
            "service": self.service,
            "service_icon_url": self.service_icon_url,
            "url": self.url,
            "subtitles": self.subtitles,
            "audio": self.audio,
        }
    
    def to_minimal_dict(self):
        """Convert the class instance to a minimal dictionary."""
        return {
            "type": self.type,
            "service": self.service,
        }


def check_watchlist(watchlist):
    full_json = []
    minimal_json = []
    movies_cnt = len(watchlist)
    for (idx, movie) in enumerate(watchlist):
        minimial_offers = []
        name = movie["Name"]

        results = search(name, "LV", "en", 1, True)[0]
        media_object = MediaObject(
            results.title,
            results.release_year,
            results.runtime_minutes,
            results.url,
            results.object_type,
            results.short_description,
            results.genres,
            results.imdb_id,
            results.poster,
            [],
        )
        offers = offers_for_countries(results.entry_id, {"LV"})["LV"]
        for offer in offers:
            type = "STREAM" if offer.monetization_type == "FLATRATE" else offer.monetization_type
            media_offer = MediaOffer(
                type,
                offer.presentation_type,
                offer.price_value,
                offer.price_currency,
                offer.package.name,
                offer.package.icon,
                offer.url,
                offer.subtitle_languages,
                offer.audio_languages,
            )
            media_object.offers.append(media_offer.to_dict())
            minimial_offers.append(media_offer.to_minimal_dict())

        full_json.append(media_object.to_dict())
        minimal_json.append({"name": media_object.title, "offers": minimial_offers})

        print(f"{idx} / {movies_cnt}")

    with open('output.json', 'w', encoding='utf-8') as file:
        json.dump(full_json, file, indent=4, ensure_ascii=False)
    with open('minimal_output.json', 'w', encoding='utf-8') as file:
        json.dump(minimal_json, file, indent=4, ensure_ascii=False)

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
        print("\t1. Check movie watchlist")
        print("\t2. View watchlist movies")

        choice = input("Choose an option (1/2): ")

        if choice == "1":
            check_watchlist(watchlist)
        elif choice == "2":
            read_minimal_result()

main()
