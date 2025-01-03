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
    print("TODO: fix incorrect years on JustWatch")

    full_json = []
    minimal_json = []
    movies_cnt = len(watchlist)
    for idx, movie in enumerate(watchlist):
        minimial_offers = []
        name = movie["Name"]
        year = movie["Year"]

        jw_search = search(name, "LV", "en", 5, True)
        jw_movie = None
        for entry in jw_search:
            if entry.title == name and str(entry.release_year) == year:
                jw_movie = entry
                break
        if not jw_movie:
            print(f"Skipping {name} ({year})")
            continue

        media_object = MediaObject(
            jw_movie.title,
            jw_movie.release_year,
            jw_movie.runtime_minutes,
            jw_movie.url,
            jw_movie.object_type,
            jw_movie.short_description,
            jw_movie.genres,
            jw_movie.imdb_id,
            jw_movie.poster,
            [],
        )
        offers = offers_for_countries(jw_movie.entry_id, {"LV"})["LV"]
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

    with open("data/output.json", "w", encoding="utf-8") as file:
        json.dump(full_json, file, indent=4, ensure_ascii=False)
    with open("data/minimal_output.json", "w", encoding="utf-8") as file:
        json.dump(minimal_json, file, indent=4, ensure_ascii=False)
