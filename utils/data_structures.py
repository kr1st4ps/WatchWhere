"""
Custom data structures used.
"""

from dataclasses import dataclass

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