from dotenv import load_dotenv
load_dotenv()

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.commons import migrate
from src.commons.postgres import database
from src.provisionings.router import router as provisionings_router
from src.sensor_readings.router import router as sensor_readings_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    await migrate.apply_pending_migrations()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://tempcheck.markusv.ch"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(provisionings_router)
app.include_router(sensor_readings_router)

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0")
