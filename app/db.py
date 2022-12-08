import pathlib

from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection


BASE_DIR = pathlib.Path(__file__).resolve().parent  # absolute path of the parent directory (regardless of the system we're on)

ASTRADB_CONNECT_BUNDLE = BASE_DIR / "unencrypted" / "astradb_connect.zip"

ASTRADB_CLIENT_ID = "<<CLIENT ID>>"
ASTRADB_CLIENT_SECRET = "<<CLIENT SECRET>>"


def get_session():
    cloud_config = {
             'secure_connect_bundle': ASTRADB_CONNECT_BUNDLE
    }
    auth_provider = PlainTextAuthProvider(ASTRADB_CLIENT_ID, ASTRADB_CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    connection.register_connection(str(session), session=session)
    connection.set_default_connection(str(session))

    return session
