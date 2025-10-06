from Services import(
    geocode_city_mock,
    get_current_weather_mock,
    get_daily_forcast_mock,
    NotFoundError
)
from Formatters import outfit_advice, wind_label, render_daily_table

def prompt_city()->str:
    return input("Enter a city: \n(New York, Dallas, Los Angeles)").strip()

def prompt_units()->str:
    u=input("Units - f or c?: ").strip().lower()
    return "fahrenheit" if u == "f" else "celcius"

def show_current(city:str,units:str):
    try:
        cw=get_current_weather_mock(city,units=units)
        print(f"\ncurrent weather for {city.title()} at {cw['time']}")
        print(f"temperature: {cw['temp']}{cw['unit_temp']} | wind: {cw['windspeed']}")
        temp_f=cw['temp'] if units == 'fahrenheit' else (cw['temp']*9/5+32)
        print(f"advice: ", outfit_advice(temp_f))
    except NotFoundError as e:
        print("error: ",e)

def show_forecast(city:str,units:str):
    try:
        f=get_daily_forcast_mock(city,days=5,units=units)
        print("\n5day forecast:")
        print(render_daily_table(f['dates'],f['highs'],f['lows'],f['unit']))
    except NotFoundError as e: print("error: ",e)

def menu():

