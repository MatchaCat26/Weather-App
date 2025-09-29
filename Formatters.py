from typing import Iterable
from codes import CODES

def farhenheit_to_celsius(f: float)->float:
    return (f-32.0)*5.0/9.0

def celsius_to_farhenheit(c: float)->float:
    return c*9.0/5.0+32.0

def outfit_advice(temp_f: float)->str:
    if temp_f>=85:return "You should wear shorts and a t-shirt"
    if temp_f<=50:return "You should wear pants and a shirt otherwise you will get sick"
    return  "You should wear pants and a t-shirt or something"

def wind_label(mph:float)->str:
    if mph>=30: return "It's very windy outside"
    if mph>=15:return "Its breezey outside"
    return "There is almost no wind outside"


