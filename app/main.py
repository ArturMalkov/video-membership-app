from fastapi import FastAPI

from app import config


app = FastAPI()
settings = config.get_settings()
