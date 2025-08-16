class FlatAd:
    def __init__(
        self, url, roommates, rent, size, district, free_from, description, publisher
    ):
        self.url = url
        self.roommates = roommates
        self.rent = rent
        self.size = size
        self.district = district
        self.free_from = free_from
        self.description = description
        self.publisher = publisher
        self.desc_summary = ""
        self.response = ""

    def __eq__(self, other):
        return self.url == other.url

    def __repr__(self):
        return f"FlatAd(url={self.url})"

    def to_string(self):
        return (
            f"FlatAd(url={self.url}, roommates={self.roommates}, "
            f"rent={self.rent}, size={self.size}, district={self.district}, "
            f"free_from={self.free_from}, description={self.description}, "
            f"publisher={self.publisher})"
        )
