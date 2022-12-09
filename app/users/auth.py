import datetime as dt

from jose import jwt, ExpiredSignatureError

from app.config import get_settings
from app.users import models


settings = get_settings()


# step 1
def authenticate(email, password):
    try:
        user = models.User.objects.get(email=email)
    except Exception:
        user = None
    else:
        if not user.verify_password(password):
            return None

    return user


# step 2
def login(user, expires=5):
    raw_data = {
        "user_id": f"{user.user_id}",
        "role": "admin",
        "exp": dt.datetime.utcnow() + dt.timedelta(seconds=expires)
    }
    return jwt.encode(raw_data, settings.secret_key, algorithm=settings.jwt_algorithm)


# step 3
def verify_user_id(token):
    data = {}

    try:
        data = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
    except ExpiredSignatureError as err:  # if expired, user should log in one more time
        print(err)
    except:
        pass

    if "user_id" not in data:
        return None

    return data
