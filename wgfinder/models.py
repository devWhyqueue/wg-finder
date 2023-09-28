class FlatAd:
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

    def __eq__(self, other):
        return self.url == other.url

    def __repr__(self):
        return f"FlatAd(url={self.url})"
