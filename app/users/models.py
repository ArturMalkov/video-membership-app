import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from app import config


settings = config.get_settings()


class User(Model):
    __keyspace__ = settings.keyspace

    email = columns.Text(primary_key=True)
    user_id = columns.UUID(primary_key=True, default=uuid.uuid1)  # UUID1 -> comes with timestamp - ideal way for storing ids in Cassandra as a distributed database
    password = columns.Text()

    def __repr__(self):
        return f"<{self.__class__.__name__}(email={self.email}, user_id={self.user_id})>"
