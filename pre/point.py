import xml.etree.ElementTree as ET
from dateutil.parser import parse as dateparse
from geopy.distance import vincenty, great_circle
from tornado.escape import json_decode, json_encode


ns = {
    'gpx': "http://www.topografix.com/GPX/1/1",
    'gpxtpx': "http://www.garmin.com/xmlschemas/TrackPointExtension/v1"
}


class Point:
    def __init__(self, lat=0, lng=0):
        self.lat = lat
        self.lng = lng
        self.alt = 0
        self.time = None
        self.user = "unknown"

        # Enriched values
        self.dist_to_goal = 0
        self.speed = 0

    def distance(self, other) -> int:
        return great_circle((self.lat, self.lng), (other.lat, other.lng)).meters

    @classmethod
    def from_json(cls, json):
        obj = json_decode(json)
        self = cls()

        self.lat = obj.get("lat")
        self.lng = obj.get("lng")
        self.timestr = obj.get("time")
        self.alt = obj.get("alt")
        self.user =obj.get("user")
        self.time = dateparse(self.timestr)

        return self

    @classmethod
    def from_gpxelem(cls, elem):
        self = Point()

        lat = elem.get('lat')
        self.lat = float(lat)

        lon = elem.get('lon')
        self.lng = float(lon)

        el = elem.find("gpx:ele", ns)
        if el is not None:
            alt = el.text
        else:
            alt = 0
        self.alt = float(alt)

        self.timestr = elem.find('gpx:time', ns).text
        self.time = dateparse(self.timestr).replace(tzinfo=None)

        return self

    @classmethod
    def from_gpxfile(cls, filename):
        et = ET.parse(filename)
        root = et.getroot()

        for track in root.findall("gpx:trk", ns):
            for seg in track.findall("gpx:trkseg", ns):
                for pt in seg.findall("gpx:trkpt", ns):
                    yield Point.from_gpxelem(pt)

    def to_json(self):
        obj = dict(
            lat=self.lat,
            lng=self.lng,
            alt=self.alt,
            time=self.timestr,
            speed=self.speed,
            user=self.user,
            distance=self.dist_to_goal
        )
        return json_encode(obj)

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return str(self)
