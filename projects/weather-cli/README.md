# Weather CLI

A small Python command-line app that looks up current weather for a place using Open-Meteo's geocoding and forecast APIs.

## Requirements
Python 3.10+ and an internet connection. No API key or third-party Python packages are required.

## Run
```bash
python weather.py "Mafikeng"
python weather.py "Cape Town" --units fahrenheit
```

The app resolves a place name to coordinates, fetches current conditions and prints a concise report. It handles unknown places, HTTP failures and missing current-weather data.

## Data source
Open-Meteo: https://open-meteo.com/ . Review its terms and attribution requirements before reusing this project in another product.
