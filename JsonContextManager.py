import scrape_weather
import json

weather_data = scrape_weather.weather_data()
with open('weather_data.json', 'w') as manager:
    json.dump(weather_data, manager, indent=4)

print(type(weather_data))
