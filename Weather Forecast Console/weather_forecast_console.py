# Use this one.
# The Google API is free as long as requests are less than 40,000 per month.
# https://mapsplatform.google.com/pricing/
# OpenWeatherMap API is 1,000 API calls per day for free.
# OpenWeatherMap API Documentation: https://openweathermap.org/api/one-call-3#current

import requests
import json
import datetime


def get_coordinates(zip_code):
    """
    Returns the latitude and longitude coordinates for a given ZIP code.

    Args:
      zip_code: The ZIP code to get coordinates for.

    Returns:
      A tuple containing the latitude and longitude coordinates, or None if the
      coordinates could not be found.
    """

    # This is the Google Maps Platform API for converting ZIP codes into latitude and longitude coordinates.
    # I have a daily limit of 1,333 set in order to keep it free.
    API_KEY_LOCATION = (
        "REDACTED"  # You can get your own API key from Google Maps Platform.
    )
    API_URL = f"https://maps.googleapis.com/maps/api/geocode/json?address={zip_code}&key={API_KEY_LOCATION}"

    # This is where the API request is made.
    response = requests.get(API_URL)
    data = json.loads(response.content)

    if response.status_code == 200 and data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    else:
        return None


def main():
    # Ask the user for their ZIP code.
    zip_code = input("Enter a ZIP code: ")

    # Pass the ZIP code into the get_coordinates function.
    coordinates = get_coordinates(zip_code)

    # Return the coordinates to the user.
    if coordinates is not None:
        latitude, longitude = coordinates
        print(
            f"The latitude and longitude coordinates for {zip_code} are {latitude}, {longitude}."
        )
    else:
        print("Could not find the coordinates for the given ZIP code.")

    # This is the OpenWeatherMap API.
    # I have a daily limit of 1,000 in order to keep it free.
    API_KEY_WEATHER = "REDACTED"  # You can get your own API key from OpenWeatherMap.
    # Notice the "latitude" and "longitude" variables are used here.
    API_URL = f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&appid={API_KEY_WEATHER}&units=metric"

    # This is where the API request is made.
    response = requests.get(API_URL)

    # Parse the JSON response.
    data = json.loads(response.content)

    # Use the parsed JSON data.
    # Notice the temperature must be converted to Fahrenheit.
    current_temperature = (data["current"]["temp"]) * 9 / 5 + 32
    print(f"The current temperature is {current_temperature} degrees Fahrenheit.")

    # Using datetime displays the days in the forecast in a human-readable format.
    # Without using datetime, the days would be displayed as a series of integers.
    daily_forecast = []
    for day in data["daily"]:
        daily_forecast.append(
            {
                "date": datetime.datetime.fromtimestamp(day["dt"]),
                "high_temp": day["temp"]["max"] * 9 / 5 + 32,
                "low_temp": day["temp"]["min"] * 9 / 5 + 32,
            }
        )

    # Print the daily high and low temperatures in Fahrenheit..
    for day in daily_forecast[:8]:
        print(
            f"Date: {day['date'].strftime('%B %d, %Y')}, High temperature: {day['high_temp']} degrees Fahrenheit, Low temperature: {day['low_temp']} degrees Fahrenheit."
        )


if __name__ == "__main__":
    main()
