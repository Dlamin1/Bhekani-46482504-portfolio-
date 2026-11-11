"""Look up current weather from Open-Meteo without an API key."""
import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

class WeatherError(Exception):
    """Expected error while retrieving weather data."""

def get_json(url):
    request = Request(url, headers={"User-Agent": "BhekaniWeatherCLI/1.0"})
    try:
        with urlopen(request, timeout=12) as response:
            return json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise WeatherError(f"Could not retrieve weather data: {exc}") from exc

def lookup(city, units="celsius"):
    geo = get_json(GEOCODING_URL + "?" + urlencode({"name": city, "count": 1, "language": "en", "format": "json"}))
    places = geo.get("results") or []
    if not places:
        raise WeatherError(f"No matching place found for {city!r}. Try a nearby larger town.")
    place = places[0]
    params = {"latitude": place["latitude"], "longitude": place["longitude"],
              "current": "temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,weather_code",
              "temperature_unit": units, "wind_speed_unit": "kmh", "timezone": "auto"}
    data = get_json(FORECAST_URL + "?" + urlencode(params))
    current = data.get("current")
    if not current:
        raise WeatherError("The weather provider did not return current conditions.")
    return place, current

def main():
    parser = argparse.ArgumentParser(description="Get current weather from Open-Meteo.")
    parser.add_argument("city", help="town or city name")
    parser.add_argument("--units", choices=("celsius", "fahrenheit"), default="celsius")
    args = parser.parse_args()
    try:
        place, weather = lookup(args.city, args.units)
    except WeatherError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    location = ", ".join(part for part in (place.get("name"), place.get("admin1"), place.get("country")) if part)
    symbol = "°C" if args.units == "celsius" else "°F"
    print(f"Current weather for {location}")
    print(f"Time: {weather.get('time', 'unknown')} ({weather.get('timezone', 'local time')})")
    print(f"Temperature: {weather['temperature_2m']}{symbol} (feels like {weather['apparent_temperature']}{symbol})")
    print(f"Humidity: {weather['relative_humidity_2m']}%")
    print(f"Wind: {weather['wind_speed_10m']} km/h")
    print(f"Weather code: {weather['weather_code']} (see Open-Meteo WMO code documentation)")
    print("\nData: Open-Meteo — https://open-meteo.com/")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
