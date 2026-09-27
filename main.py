import requests 
import tkinter as tk
from tkinter import messagebox

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    61: "Light rain",
    63: "Rain",
    65: "Heavy rain",
    71: "Snow",
    95: "Thunderstorm",

}

def get_cordinations(city_name):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name , "count": 1}
    response = requests.get(url , params=params)
    data = response.json()

    if "results"  not in data:
        return None

    result = data["results"][0]
    return result["latitude"], result["longitude"] ,result["name"]

def get_weather(latitude , longitude):
    url =  "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude" : latitude,
        "longitude": longitude,
        "current_weather": True
    }

    response = requests.get(url , params=params)
    data = response.json()
    return data["current_weather"]

def show_weather():
    city = city_entry.get().strip()

    if city == "":
        messagebox.showwarning("Input Endeed "," Please but a city name ")
        return
    coords = get_cordinations(city)
    if coords is None:
        messagebox.showerror("Not Found" , f"Could not find the city : {city}")
        return

    lat , lon , real_name = coords

    try:
        weather = get_weather(lat , lon)
    except Exception as error:
        messagebox.showerror("Error" , f"Could not fetch weather. \n{error}")
        return
    temperature = weather["temperature"]
    wind = weather["windspeed"]
    code = weather["weathercode"]
    description = WEATHER_CODES.get(code , "Unknown Condition")

    result_label.config(
        text= f"{real_name}\n"
        f"🌡 Temperature : {temperature} C\n"
        f"💨 Wind speed: {wind} km/h \n"
        f"☁ Conditions: {description}"
    )





window = tk.Tk()
window.title(" Simple Weather App")    
window.geometry("350x300")


title_label = tk.Label(
    window,
    text="Weather App",
    font=("Arial" , 18 , "bold") 
)
title_label.pack(pady=10)


city_entry = tk.Entry(
    window,
    font=("Arial" , 14),
    justify="center"
)
city_entry.pack(pady=10)
city_entry.insert(0 , "Enter a city name ")


search_button = tk.Button(
    window,
    text="Search",
    font=("Arial" , 12),
    command= show_weather 
)
search_button.pack(pady=10)

result_label = tk.Label(
    window,
    text="",
    font=("Arial" , 12) 
)
result_label.pack(pady=20)

window.mainloop()





    









