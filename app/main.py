import json
import pathlib

import uvicorn
from cassandra.cqlengine.management import sync_table
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic.error_wrappers import ValidationError

from app import config, db
from app.users.models import User
from app.users.schemas import UserLoginSchema, UserSignupSchema


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


@app.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("auth/login.html", context={"request": request})


@app.post("/login", response_class=HTMLResponse)
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    cleaned_data = UserLoginSchema(email=email, password=password)
    return templates.TemplateResponse("auth/login.html", context={"request": request})


@app.get("/signup", response_class=HTMLResponse)
def signup(request: Request):
    return templates.TemplateResponse("auth/signup.html", context={"request": request})


@app.post("/signup", response_class=HTMLResponse)
def signup(request: Request,
           email: str = Form(...),
           password: str = Form(...),
           password_confirm: str = Form(...)):
    data = {}
    error_str = ""
    try:
        cleaned_data = UserSignupSchema(email=email, password=password, password_confirm=password_confirm)
        data = cleaned_data.dict()
    except ValidationError as err:
        error_str = err.json()
    try:
        errors = json.loads(error_str)
    except Exception:
        errors = [{"loc": "non_field_error", "msg": "Unknown error"}]

    return templates.TemplateResponse("auth/signup.html", context={
        "request": request,
        "data": data,
        "errors": errors
    })


@app.get("/users")
def list_users():
    query_set = User.objects.all().limit(10)
    return list(query_set)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
