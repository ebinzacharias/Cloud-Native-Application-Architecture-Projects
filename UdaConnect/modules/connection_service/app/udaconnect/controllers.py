from flask import request
from flask_restx import Namespace, Resource
from flask_accepts import accepts, responds
from app.udaconnect.models import Connection
from app.udaconnect.schemas import ConnectionSchema
from app.udaconnect.services import ConnectionService
from typing import List

api = Namespace('Connections', description='Connection-related operations')

@api.route('/connections')
class ConnectionsResource(Resource):
    @accepts(schema=ConnectionSchema)
    @responds(schema=ConnectionSchema)
    def post(self) -> Connection:
        payload = request.get_json()
        new_connection = ConnectionService.create(payload)
        return new_connection

    @responds(schema=ConnectionSchema, many=True)
    def get(self) -> List[Connection]:
        return ConnectionService.retrieve_all()

@api.route('/connections/<int:connection_id>')
class ConnectionResource(Resource):
    @responds(schema=ConnectionSchema)
    def get(self, connection_id: int) -> Connection:
        connection = ConnectionService.retrieve(connection_id)
        return connection

