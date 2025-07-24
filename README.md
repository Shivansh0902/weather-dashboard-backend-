# Weather Dashboard Backend

A FastAPI-based backend service powering the Weather Dashboard frontend. It integrates with the OpenWeatherMap API to provide current conditions, 5-day forecasts, and geocoding lookup, all wrapped in a simple, CORS-enabled JSON API.

---

## Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Running Locally](#running-locally)
7. [API Endpoints](#api-endpoints)

   * [Root](#root)
   * [GET /weather](#get-weather)
   * [GET /forecast](#get-forecast)
   * [GET /geocode](#get-geocode)
8. [Error Handling](#error-handling)
9. [Testing](#testing)
10. [Deployment](#deployment)
11. [Contributing](#contributing)
12. [License](#license)

---

## Features

* **Current Weather**: Fetch real‑time temperature, min/max, description, and icon.
* **5-Day Forecast**: Aggregate 3‑hourly data into daily min/max values.
* **Geocoding**: Search for up to 5 matching locations (city, state, country, lat/lon).
* **CORS Enabled**: Allows any frontend to consume the API.
* **Configurable Units**: Metric (Celsius) and Imperial (Fahrenheit).

## Tech Stack

* **Python 3.13**
* **FastAPI** for building the API
* **Uvicorn** as ASGI server
* **Requests** for making HTTP calls to OpenWeatherMap
* **python-dotenv** for environment variable management

## Prerequisites

* Python 3.13 installed locally
* An [OpenWeatherMap API key](https://openweathermap.org/appid)

## Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/<your-username>/weather-dashboard-backend.git
   cd weather-dashboard-backend
   ```

2. **Create & activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate       # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   ```

## Configuration

Create a file called `.env` in the project root:

```dotenv
OPENWEATHER_API_KEY=your_openweathermap_api_key_here
```

> **Note**: Never commit your actual API key to Git.

## Running Locally

Start the Uvicorn server with autoreload:

```bash
uvicorn main:app --reload
```

By default, the app will run on [http://127.0.0.1:8000](http://127.0.0.1:8000).

## API Endpoints

### Root

```http
GET /
```

**Response**

```json
{ "message": "Hello, Weather Dashboard!" }
```

---

### GET /weather

Fetch current weather for a city or coordinates.

```http
GET /weather?city=Melbourne&units=metric
# or
GET /weather?lat=37.8&lon=-122.4&units=imperial
```

**Query Parameters**

* `city` (string): City name (e.g. `"Melbourne"`).
* `lat` & `lon` (float): Latitude & longitude (if using coordinates).
* `units` (string): `metric` or `imperial` (default: metric).

**Sample Response**

```json
{
  "city": "Melbourne",
  "country": "AU",
  "temperature": 25.24,
  "min_temp": 24.0,
  "max_temp": 27.0,
  "description": "few clouds",
  "units": "metric",
  "icon_url": "http://openweathermap.org/img/wn/02n@2x.png"
}
```

---

### GET /forecast

Fetch a 5‑day daily forecast.

```http
GET /forecast?city=Melbourne&units=metric
```

**Sample Response**

```json
{
  "city": "Melbourne",
  "country": "AU",
  "forecast": [
    { "date": "2025-07-24", "min_temp": 22.1, "max_temp": 28.5, "icon_url": "..." },
    // 5 entries total
  ]
}
```

---

### GET /geocode

Lookup up to 5 matching locations by name.

```http
GET /geocode?city=Clayton&limit=5
```

**Sample Response**

```json
[
  { "name": "Clayton", "state": "VIC", "country": "AU", "lat": -37.91, "lon": 145.13 },
  { "name": "Clayton", "state": "GA",  "country": "US", "lat": 33.53,  "lon": -82.84 }
]
```

## Error Handling

If the OpenWeather API returns an error (e.g. city not found), this service will forward the status code and message:

```json
HTTP/1.1 404 Not Found
{ "detail": "city not found" }
```

## Testing

> *No unit tests currently.*

You can manually test endpoints with `curl` or Postman.

## Deployment

### Render (recommended)

1. Sign up at [Render.com](https://render.com).
2. Create a **Web Service** → Connect GitHub → Select this repo.
3. For **Build Command**, enter:

   ```bash
   pip install -r requirements.txt
   ```
4. For **Start Command**, enter:

   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
5. In the Render dashboard, under **Environment**, set:

   ```
   OPENWEATHER_API_KEY = your_openweathermap_api_key
   ```

Render will provide a public URL like `https://weather-backend.onrender.com`.

### Other Hosts

You can also deploy to Heroku, Railway, or any container/VPS—they all support Uvicorn.

## Contributing

Feel free to open issues or PRs! Please:

* Fork the repo
* Create a feature branch
* Open a PR with a description of your changes

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.
