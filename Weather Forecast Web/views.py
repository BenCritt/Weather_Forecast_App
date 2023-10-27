from django.shortcuts import render, redirect
from django.urls import reverse
import os
import qrcode
from django.http import HttpResponse
from .forms import WeatherForm
import requests
import json
import datetime
from django.shortcuts import render
from django.core.exceptions import ValidationError
from pyzipcode import ZipCodeDatabase
from django.shortcuts import render


def get_coordinates(zip_code):
    API_KEY_LOCATION = (
        "REDACTED"  # You can get your own API key from Google Maps Platform.
    )
    API_URL = f"https://maps.googleapis.com/maps/api/geocode/json?address={zip_code}&key={API_KEY_LOCATION}"
    response = requests.get(API_URL)
    data = json.loads(response.content)
    if response.status_code == 200 and data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    else:
        return None


def get_city_and_state(zip_code):
    API_KEY_CITY = "REDACTED"  # You can get your own API key from Google Maps Platform.
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={zip_code}&key={API_KEY_CITY}"
    response = requests.get(url)
    data = json.loads(response.content)
    if response.status_code == 200 and data["status"] == "OK":
        city_name = data["results"][0]["address_components"][1]["long_name"]
        state_name = data["results"][0]["address_components"][3]["long_name"]
        return city_name, state_name
    else:
        return None


zdb = ZipCodeDatabase()


def weather(request):
    # Create a new form instance.
    form = WeatherForm(request.POST or None)

    # Get the coordinates, even if the form is not valid.
    if request.method == "POST":
        zip_code = request.POST["zip_code"]

    # If the form is valid, process the form data and render the weather forecast.
    if form.is_valid():
        coordinates = get_coordinates(zip_code)
        if coordinates == None:
            context = {
                "form": form,
                "error_message": "The ZIP code you entered is valid, but the server was unable to find coordinates for it.  This is a Google Maps Platform API error and not a problem with my code.",
            }
            return render(request, "projects/weather.html", context)
        else:
            city_name, state_name = get_city_and_state(zip_code)
            latitude, longitude = coordinates
        API_KEY_WEATHER = (
            "REDACTED"  # You can get your own API key from OpenWeatherMap.
        )
        API_URL = f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&appid={API_KEY_WEATHER}&units=metric"
        response = requests.get(API_URL)
        data = json.loads(response.content)
        daily_forecast = []
        for day in data["daily"]:
            daily_forecast.append(
                {
                    "date": datetime.datetime.fromtimestamp(day["dt"]),
                    "high_temp": int(day["temp"]["max"] * 9 / 5 + 32),
                    "low_temp": int(day["temp"]["min"] * 9 / 5 + 32),
                }
            )

        context = {
            "daily_forecast": daily_forecast[:8],
            "city_name": city_name,
            "state_name": state_name,
        }

        return render(request, "projects/weather_results.html", context)

    # If the form is not valid, render the form again.
    else:
        context = {
            "form": form,
        }
        return render(request, "projects/weather.html", context)
