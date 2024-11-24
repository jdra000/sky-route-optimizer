import requests

# API: OPENWEATHERMAP.ORG
# MY API KEY: 444942cdae0ad9dea2bd907868cb9cb5
API_KEY = '444942cdae0ad9dea2bd907868cb9cb5'

# Function to get latitude and longitude for a city
def get_city(city_name):
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},CO&appid={API_KEY}'

    response = requests.get(url)
    # Check if the response is successfull
    if response.status_code == 200:
        data = response.json()
        if data:
            city = data[0].get('name')
            lat = data[0].get('lat')
            lon = data[0].get('lon')
        return(lat, lon, city)
    else:
        return None

# Function to get important weather factors
def get_weather(city_name):
    lat, lon, city = get_city(city_name)
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}'

    response = requests.get(url)
    print(response.status_code)
    # Check if the response is successfull
    if response.status_code == 200:
        data = response.json()
        if data:
            temp = data['main'].get('temp') # Kelvin
            humidity = data['main'].get('humidity') # Humidity
            visibility = data['visibility']
            wind_speed = data['wind'].get('speed') # Wind_Speed
            clouds = data['clouds'].get('all') # Clouds %
            return {
                'general': {'city': city, 'lat': lat, 'lon': lon},
                'temp': temp,
                'humidity': humidity,
                'visibility': visibility,
                'wind_speed': wind_speed,
                'clouds': clouds
            }
    else:
        return None

print(get_weather('Apartado'))