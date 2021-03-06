from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

import ota_demo_api.consts as consts
from ota_demo_api.persistence.database import database
from ota_demo_api.routers import search

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health-check")
async def health_check():
    return {
        consts.WEB_SERVER: consts.UP
    }


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(
    search.router,
    prefix="/api/v1",
    tags=["search"],
)
