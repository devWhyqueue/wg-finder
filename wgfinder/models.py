from dataclasses import dataclass
from datetime import date


@dataclass
class FlatAd:
    url: any
    roommates: int
    rent: int
    size: int
    district: str
    free_from: date
    description: str
    desc_summary: str
    response: str
    creative_response: str

    def __init__(self, url, roommates, rent, size, district, free_from, description):
        self.url = url
        self.roommates = roommates
        self.rent = rent
        self.size = size
        self.district = district
        self.free_from = free_from
        self.description = description
        self.desc_summary = ""
        self.response = ""
        self.creative_response = ""

    def __eq__(self, other):
        return self.url == other.url
