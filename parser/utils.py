from dataclasses import dataclass

class Field:

    def __init__(self, name):
        self.name = name
        self.country = None
        self.region = None
        self.points : list(Point) = []
        self.locations : list(Location) = []

    def __str__(self):
        return f'{self.name} in {self.region}, {self.country}. Field: {len(self.points)}, Locations: {len(self.locations)}'

@dataclass
class Point:
    longitude: float
    latitude: float
    altitude: float

@dataclass
class Location:
    coord: Point
    image: str
    diagnose: str
