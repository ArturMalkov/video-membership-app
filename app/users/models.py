import uuid

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from app import config
from app.users import security, validators


settings = config.get_settings()


class User(Model):
    __keyspace__ = settings.keyspace

    email = columns.Text(primary_key=True)
    user_id = columns.UUID(primary_key=True, default=uuid.uuid1)  # UUID1 -> comes with timestamp - ideal way for storing ids in Cassandra as a distributed database
    password = columns.Text()

    def __repr__(self):
        return f"<{self.__class__.__name__}(email={self.email}, user_id={self.user_id})>"

    def set_password(self, password, commit=False):
        password_hash = security.generate_hash(password)
        self.password = password_hash

        if commit:
            self.save()

        return True

    @staticmethod
    def create_user(email, password):
        # check if email already exists in the database
        query = User.objects.filter(email=email)  # possible in Cassandra since we set email to be a pk
        if query.count() != 0:
            raise Exception("User with this email is already registered.")

        valid, message, email = validators.validate_email(email)
        if not valid:
            raise Exception(f"Invalid email: {message}")

        user = User(email=email)
        user.set_password(password)
        user.save()

        return user
