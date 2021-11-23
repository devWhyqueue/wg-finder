from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class FlatAd:
    uploaded: date
    rent: int
    size: int
    district: str
    free_from: date

    def uploaded_today(self) -> bool:
        return self.uploaded == datetime.today().date()

    def not_advertising(self) -> bool:
        return self.district[-1] != "*"
