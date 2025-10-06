import json
from pathlib import Path
from typing import Dict, Any

DATA_FILE=Path(__file__).parent/"data"/"mock_weather.json"

class NotFoundError(Exception):
    pass

def _load_data()->Dict[str,Any]:
    with open(DATA_FILE,"r",encoding="utf-8")as f:
        return json.load(f)
    
def geocode_city_mock(city:str):
    db=_load_data()
    city_key=city.strip().lower()
    for rec in db["cities"]:
        if rec["name"].lower()==city_key:
            return rec["lat"], rec["lon"], rec["name"], rec["country"]
    raise NotFoundError(f"city '{city}'not found in mock data base")

def get_current_weather_mock(city:str,units:str="fahrenheit"):
    db=_load_data()
    city_key=city.strip().lower()
    for rec in db["cities"]:
        if rec["name"].lower==city_key:
            cw=rec["current"]
            return{
                "time":cw["time"],
                "temp":cw["temp_f"]if units=="fahrenheit" else cw["temp_c"],
                "windspeed":cw["wind_mph"]if units=="fahrenheit" else cw["wind_kmh"],
                "code":cw["code"],
                "unit_temp":"°f" if units == "fahrenheit" else "c°",
                "unit_wind":"mph" if units == "fahrenheit" else "kmh"
            }
    raise NotFoundError(f"no current weather for '{city}'")

def get_daily_forcast_mock(city:str,days:int=5,units:str="fahrenheit"):
    db=_load_data()
    city_key=city.strip().lower()
    for rec in db["cities"]:
        if rec["name"].lower==city_key:
            d=rec["daily"][:days]
            dates=[x["date"]for x in d]
            highs=[x["high_f"]if units== "fahrenheit" else x["high_c"]for x in d]
            lows=[x["low_f"]if units== "fahrenheit" else x["low_c"]for x in d]
            codes=[x["code"]for x in d]
            unit="f°"if units=="fahrenheit" else "c°"
            return{
                "dates":dates,
                "highs":highs,
                "lows":lows,
                "codes":codes,
                "unit":unit,
            }
    raise NotFoundError(f"no forcast for '{city}'")