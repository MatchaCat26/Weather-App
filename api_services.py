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
            params = {"name": city ,"count":1},
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

def get_current_weather(lat:float,lon:float,*,units:str="fahrenheit")->Dict[str,Any]:
    """
    fetch current weather
    the shape of json matches the mock version
    {
    time is a string, temp is a float, wind speed is a float, code is an integer or we could have an empty code,
    unit temp is either fahrenheit or celsius, the unit wind is either in mph or kmh
    }
    """
    temp_param, wind_param, temp_label, wind_label = _unit_labels(units)
    params = {
        "latitude":lat,
        "longitude":lon,
        "current_weather":True,
        "temperature_unit":temp_param,
        "windspeed_unit":wind_param,
        "timezone":"auto"   
    }

    try:
        r=requests.get(FORECAST_URL,params=params,timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()
        j=r.json()
    except requests.RequestException as E:
        raise ApiError(f"Current Weather Failed: {E}") from E
    cw = j.get("current_weather")
    if not cw:
        raise ApiError("No Current Weather Available From API (sorry)")
    
    return{
        "time":cw.get("time"),
        "temp":float(cw["temperature"]),
        "windspeed":float(cw["windspeed"]),
        "code":cw.get("weathercode"),
        "unit_temp":temp_label,
        "unit_wind":wind_label

    }
    

def get_daily_forecast(lat:float,lon:float,*,days:int=5,units:str="fahrenheit")->Dict[str,Any]:

    """
    We're fetching the daily forecast instead of the current weather
    The shape is going to match the mock
    dates is string, highs is float, lows, is float, codes is integer, units is f or c
    """

    temp_param,_,temp_label,_ = _unit_labels(units)

    params = {
        "latitude":lat,
        "longitude":lon,
        "daily":"temperature_2m_max,temperature_2m_min,weathercode",
        "forecast_days":int(days),
        "temperature_unit":temp_param,
        "timezone":"auto"

    }

    try:
        r=requests.get(FORECAST_URL,params=params,timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()
        j=r.json()
    except requests.RequestException as E:
        raise ApiError(f"Daily Forecast Failed(sorry): {E}") from E


    d = j.get("daily") or {}
    dates = d.get("time") or []
    highs = d.get("temperature_2m_max") or []
    lows = d.get("temperature_2m_min") or []
    codes = d.get("weathercode") or []
    
    if not (dates and highs and lows):
        raise ApiError("Incomplete daily data from API")
    
#truncate to requested days :)

    dates = dates[:days]
    highs = highs[:days]
    lows = lows[:days]
    codes = codes[:days]

    return{
        "dates":dates,
        "highs":highs,
        "lows":lows,
        "codes":codes,
        "unit":temp_label
    }

if __name__ == "__main__":
    import sys
    city=(sys.argv[1]if len(sys.argv)>1 else"Dallas").strip()
    units=(sys.argv[2]if len(sys.argv)>2 else"fahrenheit").strip().lower()

    print("SELF TEST geocoding :)   ",city)
    lat, lon, name, country = geocode_city(city)
    print("--->",lat,lon,name,country)

    print("SELF TEST current :)   ")
    cw = get_current_weather(lat,lon,units=units)
    print("--->",cw)

    print("SELF TEST daily :)   ")
    f=get_daily_forecast(lat,lon,days=5,units=units)
    print("--->",{k:(v if isinstance(v,str) else v[:3]) for k,v in f.items()})