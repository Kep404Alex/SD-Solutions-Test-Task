from fastapi import FastAPI, HTTPException
from datetime import datetime
from app.db import initialize_database, add_weather_log, get_weather_logs
from app.bucket import store_weather_data, get_cached_weather
from app.weather import fetch_weather
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_database()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/weather")
async def get_weather(city: str):
    # Check cache
    cached_data = await get_cached_weather(city)
    if cached_data:
        return {"source": "cache", "data": cached_data}

    # Fetch weather from API
    weather_data = await fetch_weather(city)
    if "error" in weather_data:
        raise HTTPException(status_code=400, detail=weather_data["error"])

    # Store weather data
    timestamp = datetime.utcnow()
    file_path = await store_weather_data(city, weather_data, timestamp)

    # Add to DynamoDB
    await add_weather_log(city, timestamp, file_path)

    return {"source": "api", "data": weather_data}

@app.get("/logs")
async def get_logs(city: str):
    logs = await get_weather_logs(city)
    if not logs:
        raise HTTPException(status_code=404, detail="No logs found")
    return logs
