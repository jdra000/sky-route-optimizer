import asyncio
import aiohttp

import os
from dotenv import load_dotenv

# API: OPENWEATHERMAP.ORG
load_dotenv()
api_key = os.getenv('API_KEY')

# AVAILABILITY VS WEATHER FACTORS:
# CLOUDS > 50 = -1, CLOUDS > 70 = -2, CLOUDS > 90 = CLOSED
# HUMIDITY > 80 = -1, HUMIDTY > 95 = CLOSED
# TEMP < 270 = -1, TEMP < 250 = -3
# VISIBILITY < 10000 = -2, VISIBILITY < 8000 = CLOSED
# WIND_SPEED > 2.5 = -1, WIND_SPEED > 3 = -3


class API:
    def __init__(self, api_key):
        self.city_codes = {
            'bucaramanga':'BGA', 
            'bogota':'BOG', 
            'medellin':'MDE', 
            'cucuta':'CUC', 
            'barrancabermeja':'BAC',
            'yopal':'EYP', 
            'neiva':'NVA', 
            'armenia':'AXM', 
            'cartago':'CRC', 
            'quibdo':'UIB', 
            'apartado':'APO', 
            'monteria':'MTR', 
            'cartagena':'CTG'
        }
        self.report = {}
        self.api_key = api_key

    async def main(self):
        async with aiohttp.ClientSession() as session:
            # First task: Fetch coordinates for each city
            async with asyncio.TaskGroup() as tg:
                tasks = {city: tg.create_task(self.get_coordinates(session, city)) for city in self.city_codes.keys()}
            coordinates = {city: {'lat': task.result()[0], 'lon': task.result()[1]} for city, task in tasks.items()}
            
            # Second task: Build weather report for each city
            async with asyncio.TaskGroup() as tg:
                tasks = {city: tg.create_task(self.get_weather_report(session, coordinate)) for city, coordinate in zip(self.city_codes.values(), coordinates.values())}
            final_report = {city : task.result() for city, task in tasks.items()}
            
        return final_report

    # Method to get latitude and longitude for a city
    async def get_coordinates(self, session, city_name):
        url = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},CO&appid={self.api_key}'
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
            # Check if the response is successfull
                if data:
                    lat = data[0].get('lat')
                    lon = data[0].get('lon')
                else:
                    print(f'No data was found for {city_name}')
                    return None
            return lat, lon

    async def get_weather_report(self, session, coordinate):
        lat, lon = coordinate.get('lat'), coordinate.get('lon')
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={self.api_key}'

        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                print(data)
                if data:

                    risks = 0
                    cloud_conditions = data['clouds'].get('all')
                    temp_conditions = data['main'].get('temp')
                    humidity_conditions = data['main'].get('humidity')
                    visibility_conditions = data['visibility']
                    wind_conditions = data['wind'].get('speed')

                    # START CHECKING
                    if cloud_conditions > 70:
                        risks -= 1
                    if humidity_conditions > 70:
                        risks -= 2
                    if visibility_conditions < 10000:
                        risks -= 3
                    if wind_conditions > 5.1:
                        risks -= 4

                    return risks