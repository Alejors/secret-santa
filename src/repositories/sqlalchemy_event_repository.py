from .base_repository import SQLAlchemyBaseRepository
from src.models import EventModel
from src.entities import Event


class SQLAlchemyEventsRepository(SQLAlchemyBaseRepository):
    def __init__(self, sqlalchemy_client):
        super().__init__(sqlalchemy_client, EventModel, Event)
