import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import router


def configure_logging():
    level_name = os.getenv("MIND_DEBUG", "0")
    level = logging.DEBUG if level_name == "1" else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s")


configure_logging()

app = FastAPI(title="MIND PoC Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
