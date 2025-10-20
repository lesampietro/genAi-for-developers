import sys
import requests

def weather(city: str = "São Paulo") -> None:
    """receives a city name as an argument form the command line and prints the current weather information. if no argument is passed, uses 'São Paulo' as default"""
    response1 = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1")
    data = response1.json()
    country = data["results"][0]["country"]
    lat = data["results"][0]["latitude"]
    lon = data["results"][0]["longitude"]

    response2 = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m")
    data = response2.json()
    temperature = data["current"]["temperature_2m"]

    print(f"Current temperature in {city}, {country} is {temperature}°C!")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            weather(arg)
    else:
        weather()