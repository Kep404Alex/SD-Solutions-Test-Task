import aiofiles
from pathlib import Path
import time

CACHE_DURATION = 300  # 5 minutes
BUCKET_DIR = Path("data")

BUCKET_DIR.mkdir(exist_ok=True)

async def store_weather_data(city: str, data: dict, timestamp):
    # Format the timestamp to remove invalid characters
    sanitized_timestamp = timestamp.strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{city}_{sanitized_timestamp}.json"
    file_path = BUCKET_DIR / file_name

    async with aiofiles.open(file_path, mode="w") as f:
        await f.write(str(data))
    return str(file_path)

async def get_cached_weather(city: str):
    for file in BUCKET_DIR.glob(f"{city}_*.json"):
        if time.time() - file.stat().st_mtime < CACHE_DURATION:
            async with aiofiles.open(file, mode="r") as f:
                return eval(await f.read())  # Load JSON
    return None
