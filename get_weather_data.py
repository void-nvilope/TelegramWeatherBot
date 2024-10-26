import aiohttp
from config import OPEN_WEATHER_TOKEN

"""Парсинг данных по api по названию города/местности"""
async def get_weather_in_city(city_name):
    async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={OPEN_WEATHER_TOKEN}&units=metric"
                                ) as res_weather:
                    data = await res_weather.json()
    
    return res_weather.status, data

"""Парсинг данных по api по широте и долготе"""
async def get_coordinates_city(lat, lon):
    async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPEN_WEATHER_TOKEN}&units=metric&lang=ru"
                                ) as res_weather:
                    data = await res_weather.json()
    
    return data

"""Парсинг данных по api погоды на 5 дней"""
async def get_weather_five_days(city):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPEN_WEATHER_TOKEN}&units=metric"
                               ) as res_weather:
            data = await res_weather.json()
            
    return data