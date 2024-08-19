import os

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])
load_dotenv()
HOST = os.environ.get("HOST") or "127.0.0.1"
PORT = int(str(os.environ.get("PORT"))) or 5173

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


def main():
    uvicorn.run(app, host=HOST, port=PORT)
