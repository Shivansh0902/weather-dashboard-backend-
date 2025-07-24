from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from datetime import datetime
import os, requests

# 1) Load .env
load_dotenv()

# 2) Read your key
API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise RuntimeError("OPENWEATHER_API_KEY not set in .env")

app = FastAPI()

##── Add this block ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # for prod, lock this down to your deployed frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#────────────────────


# 3) Test endpoint
@app.get("/")
async def root():
    return { "message": "Hello, Weather Dashboard!" }

# 4) Real weather endpoint
@app.get("/weather")
async def get_weather(
    city: str | None = None,
    lat: float | None = None,
    lon: float | None = None,
    units: str = "metric"
):
    # Build URL by city or by coordinates
    if lat is not None and lon is not None:
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}&lon={lon}&units={units}&appid={API_KEY}"
        )
    else:
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&units={units}&appid={API_KEY}"
        )
    resp = requests.get(url)
    if resp.status_code != 200:
        detail = resp.json().get("message", "Failed to fetch weather")
        raise HTTPException(status_code=resp.status_code, detail=detail)
    data = resp.json()
    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "min_temp": data["main"]["temp_min"],
        "max_temp": data["main"]["temp_max"],
        "description": data["weather"][0]["description"],
        "units": units,
        "icon_url": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
    }

@app.get("/forecast")
async def get_forecast(
    city: str | None = None,
    lat: float | None = None,
    lon: float | None = None,
    units: str = "metric"
):
    # Build URL by city or by coordinates
    if lat is not None and lon is not None:
        url = (
            "https://api.openweathermap.org/data/2.5/forecast"
            f"?lat={lat}&lon={lon}&units={units}&appid={API_KEY}"
        )
    else:
        url = (
            "https://api.openweathermap.org/data/2.5/forecast"
            f"?q={city}&units={units}&appid={API_KEY}"
        )
    resp = requests.get(url)
    if resp.status_code != 200:
        detail = resp.json().get("message", "Failed to fetch forecast")
        raise HTTPException(status_code=resp.status_code, detail=detail)
    data = resp.json()

    # Group 3‑hourly entries into daily min/max
    daily = {}
    for entry in data["list"]:
        date = entry["dt_txt"].split(" ")[0]  # e.g. "2025-07-24"
        temp = entry["main"]["temp"]
        icon = entry["weather"][0]["icon"]
        if date not in daily:
            daily[date] = {"min": temp, "max": temp, "icon": icon}
        else:
            daily[date]["min"] = min(daily[date]["min"], temp)
            daily[date]["max"] = max(daily[date]["max"], temp)

    # Take the first 5 unique dates
    dates = sorted(daily.keys())[:5]
    forecast = [
        {
            "date": d,
            "min_temp": daily[d]["min"],
            "max_temp": daily[d]["max"],
            "icon_url": f"http://openweathermap.org/img/wn/{daily[d]['icon']}@2x.png"
        }
        for d in dates
    ]
    return {
        "city": data["city"]["name"],
        "country": data["city"]["country"],
        "forecast": forecast,
        "units": units
    }


@app.get("/geocode")
async def geocode(city: str, limit: int = 5):
    """
    Return up to `limit` locations matching `city`,
    each with name, state (if any), country, lat & lon.
    """
    url = (
        "http://api.openweathermap.org/geo/1.0/direct"
        f"?q={city}&limit={limit}&appid={API_KEY}"
    )
    resp = requests.get(url)
    if resp.status_code != 200:
        detail = resp.json().get("message", "Failed to geocode")
        raise HTTPException(status_code=resp.status_code, detail=detail)

    results = resp.json()
    # Map to only the fields we need
    return [
        {
            "name": item["name"],
            "state": item.get("state"),
            "country": item["country"],
            "lat": item["lat"],
            "lon": item["lon"]
        }
        for item in results
    ]
