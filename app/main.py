import uvicorn
from cassandra.cqlengine.management import sync_table
from fastapi import FastAPI

from app import config, db
from app.users.models import User


app = FastAPI()
DB_SESSION = None
settings = config.get_settings()


@app.on_event("startup")
def on_startup():
    # triggered when FastAPI starts
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)


@app.on_event("shutdown")
def on_shutdown():
    pass


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
