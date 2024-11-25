import requests
import asyncio
import aiohttp

# API: OPENWEATHERMAP.ORG
# MY API KEY: 444942cdae0ad9dea2bd907868cb9cb5
API_KEY = '444942cdae0ad9dea2bd907868cb9cb5'

# AVAILABILITY VS WEATHER FACTORS:
# CLOUDS > 50 = -1, CLOUDS > 70 = -2, CLOUDS > 90 = CLOSED
# HUMIDITY > 80 = -1, HUMIDTY > 95 = CLOSED
# TEMP < 270 = -1, TEMP < 250 = -3
# VISIBILITY < 10000 = -2, VISIBILITY < 8000 = CLOSED
# WIND_SPEED > 2.5 = -1, WIND_SPEED > 3 = -3

class API:
    def __init__(self):
        self.cities = ['bucaramanga', 'bogota', 'medellin', 'cucuta', 'barrancabermeja',
           'yopal', 'neiva', 'armenia', 'cartago', 'quibdo', 'apartado', 
           'monteria', 'cartagena']
        self.nodes = ['BGA', 'BOG', 'MDE', 'CUC', 'BAC', 'EYP',
         'NVA', 'AXM', 'CRC', 'UIB', 'APO', 'MTR',
         'CTG']
        self.report = {}

    # Method to get latitude and longitude for a city
    async def get_coordinates(self, session, city_name):
        url = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},CO&appid={API_KEY}'
        async with session.get(url) as response:
            data = await response.json()
            # Check if the response is successfull
            if data:
                lat = data[0].get('lat')
                lon = data[0].get('lon')
            return lat, lon

    async def main(self):
        async with aiohttp.ClientSession() as session:
            # First task: Fetch coordinates for each city
            coordinates_tasks = [asyncio.ensure_future(self.get_coordinates(session, city)) for city in self.cities]
            coordinates = await asyncio.gather(*coordinates_tasks)

            self.report = {city: {'coordinates': {'lat': lat, 'lon': lon}} for city, (lat, lon) in zip(self.cities, coordinates)}
            
            # Second task: Build weather report for each city
            weather_report_tasks = [asyncio.ensure_future(self.get_weather_report(session, city)) for city in self.report.keys()]
            reports = await asyncio.gather(*weather_report_tasks)
            final_report = {self.nodes[i] : risk for i, risk in enumerate(reports)}
            
        return final_report


    async def get_weather_report(self, session, city):
        lat, lon = self.report[city]['coordinates'].get('lat'), self.report[city]['coordinates'].get('lon')
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}'

        async with session.get(url) as response:
            data = await response.json()
            if data:

                risks = 0
                cloud_conditions = data['clouds'].get('all')
                temp_conditions = data['main'].get('temp')
                humidity_conditions = data['main'].get('humidity')
                visibility_conditions = data['visibility']
                wind_conditions = data['wind'].get('speed')

                # START CHECKING
                if cloud_conditions > 50 and temp_conditions < 270:
                    risks -= 1
                if humidity_conditions > 90:
                    risks -=2
                if visibility_conditions < 10000:
                    risks -= 1
                if wind_conditions > 0.3:
                    risks -= 1

                return risks

    # Method to get important weather factors
    def get_weather(self, city_name):
        lat, lon = self.get_city(city_name)
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}'

        response = requests.get(url)
        print(response.status_code)
        # Check if the response is successfull
        if response.status_code == 200:
            data = response.json()
            if data:
                temp = data['main'].get('temp') # Kelvin
                humidity = data['main'].get('humidity') # Humidity
                visibility = data['visibility'] # Visibility
                wind_speed = data['wind'].get('speed') # Wind_Speed
                clouds = data['clouds'].get('all') # Clouds %


                return {
                    'lat': lat,
                    'lon': lon,
                    'temp': temp,
                    'humidity': humidity,
                    'visibility': visibility,
                    'wind_speed': wind_speed,
                    'clouds': clouds
                }
        else:
            return None
        
    def generate_report(self):
        report = {}
        for city in self.cities:
            conditions = self.get_weather(city)

            risks = 0
            cloud_conditions = conditions['clouds']
            temp_conditions = conditions['temp']
            humidity_conditions = conditions['humidity']
            visibility_conditions = conditions['visibility']
            wind_conditions = conditions['wind_speed']
            # START CHECKING
            if cloud_conditions > 50 and temp_conditions < 270:
                risks -= 1
            if humidity_conditions > 90:
                risks -=2
            if visibility_conditions < 10000:
                risks -= 1
            if wind_conditions > 0.3:
                risks -= 1

            if city not in report:
                report[city] = 0
            report[city] = risks
            # REPLACE NAME BY 3 LETTER CODE
            final_report = {self.nodes[i]:value for i, value in enumerate(report.values())}

        return final_report

api = API()
print(asyncio.run(api.main()))