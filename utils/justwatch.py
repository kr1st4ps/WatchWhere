"""
Functions using the JustWatch lib.
"""

import json

from simplejustwatchapi.justwatch import search, offers_for_countries
from utils.data_structures import MediaObject, MediaOffer


def check_watchlist(watchlist):
    """
    Checks and saves all services for movies in the watchlist.
    """

    full_json = []
    minimal_json = []
    movies_cnt = len(watchlist)
    for idx, movie in enumerate(watchlist):
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
            monetization_type = (
                "STREAM"
                if offer.monetization_type == "FLATRATE"
                else offer.monetization_type
            )
            media_offer = MediaOffer(
                monetization_type,
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

    with open("output.json", "w", encoding="utf-8") as file:
        json.dump(full_json, file, indent=4, ensure_ascii=False)
    with open("minimal_output.json", "w", encoding="utf-8") as file:
        json.dump(minimal_json, file, indent=4, ensure_ascii=False)
