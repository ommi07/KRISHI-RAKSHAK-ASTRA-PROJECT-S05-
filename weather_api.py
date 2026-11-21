"""
Weather data and alert simulation utilities.

Fetches current weather from the Open-Meteo API (no API key required)
and provides a cached fallback if the request fails or the device is offline.
"""

import requests


def get_live_weather(lat, lon):
    """Return current weather for the supplied latitude and longitude."""
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,rain,wind_speed_10m"
    )

    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        data = res.json()["current"]

        return {
            "temp": data["temperature_2m"],
            "humidity": data["relative_humidity_2m"],
            "rain": data["rain"],
            "wind": data["wind_speed_10m"],
            "source": "Live (Open-Meteo)",
        }

    except Exception:
        # Offline fallback so the demo can continue without a network connection.
        return {
            "temp": 29.5,
            "humidity": 64,
            "rain": 2.0,
            "wind": 14.0,
            "source": "Cached Fallback",
        }


def apply_alert_simulation(weather, base_ndvi, base_ndwi, sim_mode):
    """
    Apply simulated weather-event conditions and adjust NDVI/NDWI values.

    Returns:
        tuple: (updated_weather, updated_ndvi, updated_ndwi)
    """
    w = weather.copy()
    ndvi, ndwi = base_ndvi, base_ndwi

    if sim_mode == "Cyclone Alert":
        w["wind"], w["rain"], w["humidity"] = 95.0, 85.0, 92
        ndwi = min(0.85, base_ndwi + 0.45)
        ndvi = max(0.15, base_ndvi - 0.15)

    elif sim_mode == "Hailstorm & Heavy Rain":
        w["wind"], w["rain"], w["humidity"] = 58.0, 62.0, 88
        ndwi = min(0.75, base_ndwi + 0.30)
        ndvi = max(0.20, base_ndvi - 0.18)

    elif sim_mode == "Severe Drought":
        w["temp"], w["rain"], w["humidity"] = 43.0, 0.0, 22
        ndwi = max(-0.60, base_ndwi - 0.35)
        ndvi = max(0.12, base_ndvi - 0.28)

    return w, round(ndvi, 2), round(ndwi, 2)

def search_indian_location(place_name):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={place_name}&count=1&countryCode=IN"
    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        results = res.json().get("results")
        if not results:
            return None
        loc = results[0]
        state = loc.get("admin1", "India")

        if state in ("Rajasthan", "Gujarat"):
            pest, ndvi, ndwi = "Desert Locust", 0.38, -0.12
        elif state in ("Odisha", "West Bengal", "Andhra Pradesh", "Tamil Nadu", "Kerala"):
            pest, ndvi, ndwi = "Brown Planthopper", 0.65, 0.30
        else:
            pest, ndvi, ndwi = "Stem Borer & Aphids", 0.58, 0.15

        return {
            "name": f"{loc['name']}, {state}",
            "lat": loc["latitude"],
            "lon": loc["longitude"],
            "base_ndvi": ndvi,
            "base_ndwi": ndwi,
            "main_pest": pest
        }
    except Exception:
        return None