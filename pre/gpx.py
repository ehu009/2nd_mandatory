import xml.etree.ElementTree as ET
from dateutil.parser import parse
from geopy.distance import vincenty


ns = {
    'gpx': "http://www.topografix.com/GPX/1/1",
    'gpxtpx': "http://www.garmin.com/xmlschemas/TrackPointExtension/v1"
}


class GpxPoint:
    def __init__(self, elem):
        self.elem = elem

    @property
    def latitude(self):
        lat = self.elem.get('lat')
        return float(lat)

    @property
    def longitude(self):
        lon = self.elem.get('lon')
        return float(lon)

    @property
    def altitude(self):
        el = self.elem.find("gpx:ele", ns)
        if el:
            alt = el.text
        else:
            alt = 0
        return float(alt)

    @property
    def time(self):
        text = self.elem.find('gpx:time', ns).text
        dt = parse(text).replace(tzinfo=None)
        return dt

    def distance(self, other) -> int:
        return vincenty((self.lat, self.lng), (other.lat, other.lng)).meters

    def __str__(self):
        return f"{self.latitude},{self.longitude}"

    def __repr__(self):
        return str(self)



class GpxFile:
    def __init__(self, filename):
        et = ET.parse(filename)
        self.root = et.getroot()

    def __iter__(self):
        for track in self.root.findall("gpx:trk", ns):
            for seg in track.findall("gpx:trkseg", ns):
                for pt in seg.findall("gpx:trkpt", ns):
                    yield GpxPoint(pt)
