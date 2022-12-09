import pathlib

import uvicorn
from cassandra.cqlengine.management import sync_table
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app import config, db
from app.users.models import User


BASE_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"

app = FastAPI()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

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


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    context = {
        "request": request,  # required to use Jinja2
        "abc": 123
    }
    return templates.TemplateResponse("home.html", context=context)


@app.get("/users")
def list_users():
    query_set = User.objects.all().limit(10)
    return list(query_set)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
