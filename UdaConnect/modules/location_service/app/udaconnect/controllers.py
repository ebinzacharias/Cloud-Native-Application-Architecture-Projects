from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema
from app.udaconnect.services import LocationService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource

# Create a new namespace for Location resources
api = Namespace("locations", description="Location-related operations")

@api.route("/locations")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self):
        """Create a new location."""
        location_data = request.get_json()
        location = LocationService.create(location_data)
        return location

    @responds(schema=LocationSchema, many=True)
    def get(self):
        """Get all locations."""
        locations = LocationService.retrieve_all()
        return locations

@api.route("/locations/<int:location_id>")
@api.param("location_id", "Location ID")
class LocationDetailResource(Resource):
    @responds(schema=LocationSchema)
    def get(self, location_id):
        """Get a single location by ID."""
        location = LocationService.retrieve(location_id)
        return location

