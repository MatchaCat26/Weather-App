from __future__ import annotations
import requests
from typing import Tuple,Dict,Any

GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
DEFAULT_TIMEOUT = 10

class ApiError(Exception):
    """it's for api network and data errors"""
    pass

def _unit_labels(units:str)->Tuple[str,str,str,str]:
    """we're returning the temp unit peram, the wind unit peram, the temp label, and the wind label"""
    is_f=(units=="fahrenheit")
    return(
        "fahrenheit"if is_f else "celsius",
        "mph"if is_f else "kmh",
        "f"if is_f else "c",
        "mph"if is_f else "km/h",
    )

def geocode_city(city:str)->Tuple[float,float,str,str]:
    """Geocode a city name
    
    returns lat, lon, display name, and country"""
    if not city or not city.strip():
        raise ApiError("city name cannot be empty")
    try:
        r = requests.get(
            GEO_URL,
            parems = {"name": city ,"count":1},
            timeout = DEFAULT_TIMEOUT
        )
        r.raise_for_status()
        data = r.json()
    except requests.RequestException as E:
        raise ApiError(f"geocoding failed: {E}") from E
    results = data.get("results") or []
    if not results:
        raise ApiError(f"city {city} not found")
    top = results[0]
    lat = float(top["latitude"])
    lon = float(top["longitude"])
    name = str(top.get("name",city).strip())
    country = str(top.get("country","").strip())
    return lat, lon,name,country

def get_current_weather

def get_daily_forecast