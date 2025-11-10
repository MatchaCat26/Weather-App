from Formatters import outfit_advice, wind_label, render_daily_table

USE_LIVE = True
if USE_LIVE:
    from api_services import (geocode_city, get_current_weather, get_daily_forecast, ApiError as DataError)
else: 
    from services import(
    geocode_city_mock as geocode_city,
    get_current_weather_mock as get_current_weather,
    get_daily_forcast_mock as get_daily_forecast,
    NotFoundError as DataError
)

def prompt_city()->str:
    s=input("Enter a city: (New York, Dallas, Los Angeles)").strip()
    print("[OK] City set to: ",repr(s))
    return s 

def prompt_units()->str:
    u=input("Units - f or c?: ").strip().lower()
    if u in ("c","cel","celsius"):
        print("[OK] Units set to celsius")
        return "celsius"
    print("[OK] Units set to fahrenheit")
    return "fahrenheit"

def show_current(city:str,units:str):
    try:
        if USE_LIVE:
            lat, lon, name, country = geocode_city(city)
            cw = get_current_weather(lat, lon, units=units)
            display_name = f"{name}, {country}".strip().strip(",")
            print (f"DEBUG lve current:{lat=},{lon=},{display_name}   |  debug the bug")
        else:
            cw=get_current_weather(city,units=units)
            display_name = city.title()
        print(f"\ncurrent weather for {display_name} at {cw['time']}")
        print(f"temperature: {cw['temp']}{cw['unit_temp']} | wind: {cw['windspeed']}")
        temp_f=cw['temp'] if units == 'fahrenheit' else (cw['temp']*9/5+32)
        print(f"advice: ", outfit_advice(temp_f))
        print(f"wind: ",wind_label (cw['windspeed']))
    except DataError as e:
        print("error: ",e)

def show_forecast(city:str,units:str):
    try:
        if USE_LIVE:
            lat,lon,name,country=geocode_city(city)
            f=get_daily_forecast(lat,lon,days=5,units=units)
            print (f"DEBUG lve current:{lat=},{lon=},city={name},{country}   |  debug the bug")
        else:
            f=get_daily_forecast(city,days=5,units=units)
        print("[DEBUG] City sent to forecast: ",repr(city),"|units: ",repr(units))
        print("\n5day forecast:")
        print(render_daily_table(f['dates'],f['highs'],f['lows'],f['unit']))
    except DataError as e: print("error: ",e)

def menu():
    print("THE WEATHER APP :)")
    city=prompt_city()
    units=prompt_units()

    while True:
        print("\nmenu\n1. Current Weather\n2. 5 Day Forecast\n3. Change City\n4. Chagne Units\n5. Quit")
        choice=input("choose: ").strip()
        print ("[DEBUG] Choice = ",repr(choice))
        if choice=="1":
            show_current(city,units)
        elif choice=="2":
            show_forecast(city,units)
        elif choice=="3":
            city=prompt_city()
        elif choice=="4":
            units=prompt_units()
        elif choice=="5":
            print("GOODBYE FOREVER AND EVER AND EVER :(");break
        else:
            print("PLEASE PRINT A NUMBER 1-5 OR ELSE BEGONE")

if __name__=="__main__":
    menu()