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

    def __eq__(self, other):
        return self.url == other.url
