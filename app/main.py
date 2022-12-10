import uvicorn
from cassandra.cqlengine.management import sync_table
from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse

from app import config, db, utils, shortcuts
from app.users.models import User
from app.users.schemas import UserLoginSchema, UserSignupSchema


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


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    context = {
        "request": request,  # required to use Jinja2
        "abc": 123
    }
    return shortcuts.render(request, "home.html", context)


@app.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return shortcuts.render(request, "auth/login.html", context={})


@app.post("/login", response_class=HTMLResponse)
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    raw_data = {"email": email, "password": password}
    data, errors = utils.valid_schema_data_or_error(raw_data, UserLoginSchema)
    context = {
            "data": data,
            "errors": errors
    }
    if len(errors) > 0:
        return shortcuts.render(request, "auth/login.html", context=context, status_code=status.HTTP_404_NOT_FOUND)

    return shortcuts.render(request, "auth/login.html", context=context)


@app.get("/signup", response_class=HTMLResponse)
def signup(request: Request):
    return shortcuts.render(request, "auth/signup.html", context={})


@app.post("/signup", response_class=HTMLResponse)
def signup(request: Request,
           email: str = Form(...),
           password: str = Form(...),
           password_confirm: str = Form(...)):
    raw_data = {"email": email, "password": password, "password_confirm": password_confirm}
    data, errors = utils.valid_schema_data_or_error(raw_data, UserSignupSchema)
    context = {
        "data": data,
        "errors": errors
    }
    if len(errors) > 0:
        return shortcuts.render(request, "auth/signup.html", context=context, status_code=status.HTTP_404_NOT_FOUND)

    return shortcuts.render(request, "auth/signup.html", context)


@app.get("/users")
def list_users():
    query_set = User.objects.all().limit(10)
    return list(query_set)


if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
