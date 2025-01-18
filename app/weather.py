import httpx

API_KEY = "9159bc2841d0c7c473745007fb77a724"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

async def fetch_weather(city: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(BASE_URL, params={"q": city, "appid": API_KEY})
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"API error: {e.response.text}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
