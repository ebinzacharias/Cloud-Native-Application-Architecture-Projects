from app import db
from sqlalchemy import Column, Integer, String, DateTime
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from shapely.geometry import Point

class Location(db.Model):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, nullable=False)
    coordinate = Column(Geometry("POINT"), nullable=False)
    creation_time = Column(DateTime, nullable=False)

    def set_coordinates(self, lat, lon):
        self.coordinate = f"ST_Point({lon}, {lat})"

    @property
    def wkt_shape(self):
        point = to_shape(self.coordinate)
        return point.wkt

