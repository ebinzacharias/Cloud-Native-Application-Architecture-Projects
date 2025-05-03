from app import db
from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from datetime import datetime

class LocationService:
    @staticmethod
    def create(location_data):
        """Create a new location."""
        location = Location(**location_data)
        db.session.add(location)
        db.session.commit()
        return location

    @staticmethod
    def retrieve(location_id):
        """Retrieve a location by ID."""
        return db.session.query(Location).get(location_id)

    @staticmethod
    def retrieve_all():
        """Retrieve all locations."""
        return db.session.query(Location).all()

