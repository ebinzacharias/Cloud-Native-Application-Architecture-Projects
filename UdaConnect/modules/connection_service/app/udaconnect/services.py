from app import db
from app.udaconnect.models import Connection
from app.udaconnect.schemas import ConnectionSchema
from typing import Dict, List

class ConnectionService:
    @staticmethod
    def create(connection_data: Dict) -> Connection:
        new_connection = Connection(**connection_data)
        db.session.add(new_connection)
        db.session.commit()
        return new_connection

    @staticmethod
    def retrieve(connection_id: int) -> Connection:
        return db.session.query(Connection).get(connection_id)

    @staticmethod
    def retrieve_all() -> List[Connection]:
        return db.session.query(Connection).all()

