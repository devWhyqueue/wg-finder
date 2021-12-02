from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class FlatAd:
    url: any
    roommates: int
    uploaded: date
    rent: int
    size: int
    district: str
    free_from: date

    def uploaded_today(self) -> bool:
        return self.uploaded == datetime.today().date()

    def only_advertising(self) -> bool:
        return self.district[-1] == "*"

    def too_cheap(self) -> bool:
        return self.rent < 100
