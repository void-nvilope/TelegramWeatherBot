import dictionary as d
from aiogram.types import Message, CallbackQuery
import keyboards as kb
import datetime
from aiogram import html

"""Вывод полученной информации о погоде"""
async def output_weather(message: Message, data, city):
    weather_description = data['weather'][0]['main']
            
    if weather_description in d.code_to_smile:
        wd = d.code_to_smile[weather_description]
    else:
        wd = ''
    
    cur_weather = round(data['main']['temp'], 1); prefix = '+' if cur_weather >= 1.0 else ''
    humidity = data['main']['humidity']
    pressure = round(data['main']['pressure'] / 1.33322)
    wind = data['wind']['speed']

    sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'] + data['timezone'], tz=datetime.timezone.utc)
    sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'] + data['timezone'], tz=datetime.timezone.utc)
    length_day = sunset_timestamp - sunrise_timestamp
    
    await message.answer(
        f"🗓 {html.bold(d.weather_indicators[8])} {html.italic(datetime.datetime.now().strftime('%d.%m.%Y %H:%M'))} 🗓\n\n\n"
        f"🌍 {html.bold(d.weather_indicators[0])} {html.italic(city.title())}\n\n"
        f"🌡 {html.bold(d.weather_indicators[1])} {prefix}{cur_weather}°C {html.bold(wd)}\n\n"
        f"💧 {html.bold(d.weather_indicators[2])} {humidity}%\n\n"
        f"🗿 {html.bold(d.weather_indicators[3])} {pressure} мм.рт.ст\n\n"
        f"🍃 {html.bold(d.weather_indicators[4])} {wind} м/с\n\n"
        f"🌅 {html.bold(d.weather_indicators[5])} {sunrise_timestamp.strftime('%H:%M')}\n\n"
        f"🌇 {html.bold(d.weather_indicators[6])} {sunset_timestamp.strftime('%H:%M')}\n\n"
        f"☀ {html.bold(d.weather_indicators[7])} {str(length_day)[:1]} ч. {str(length_day)[2:4]} м."
    )

"""Вывод полученной информации о погоде на 5 дней"""
async def output_weather_five_days(callback: CallbackQuery, data, city):
    date_1 = datetime.datetime.fromtimestamp(data['list'][0]['dt'], tz=datetime.timezone.utc).strftime('%d.%m.%Y')
    temp_1 = round(data['list'][0]['main']['temp'], 1); weather_1 = data['list'][0]['weather'][0]['main']
    humidity_1 = data['list'][0]['main']['humidity']; wind_1 = round(data['list'][0]['wind']['speed'], 1)
    
    date_2 = datetime.datetime.fromtimestamp(data['list'][8]['dt'], tz=datetime.timezone.utc).strftime('%d.%m.%Y')
    temp_2 = round(data['list'][8]['main']['temp'], 1); weather_2 = data['list'][8]['weather'][0]['main']
    humidity_2 = data['list'][8]['main']['humidity']; wind_2 = round(data['list'][8]['wind']['speed'], 1)
    
    date_3 = datetime.datetime.fromtimestamp(data['list'][16]['dt'], tz=datetime.timezone.utc).strftime('%d.%m.%Y')
    temp_3 = round(data['list'][16]['main']['temp'], 1); weather_3 = data['list'][16]['weather'][0]['main']
    humidity_3 = data['list'][16]['main']['humidity']; wind_3 = round(data['list'][16]['wind']['speed'], 1)
    
    date_4 = datetime.datetime.fromtimestamp(data['list'][24]['dt'], tz=datetime.timezone.utc).strftime('%d.%m.%Y')
    temp_4 = round(data['list'][24]['main']['temp'], 1); weather_4 = data['list'][24]['weather'][0]['main']
    humidity_4 = data['list'][24]['main']['humidity']; wind_4 = round(data['list'][24]['wind']['speed'], 1)
    
    date_5 = datetime.datetime.fromtimestamp(data['list'][32]['dt'], tz=datetime.timezone.utc).strftime('%d.%m.%Y')
    temp_5 = round(data['list'][32]['main']['temp'], 1); weather_5 = data['list'][32]['weather'][0]['main']
    humidity_5 = data['list'][32]['main']['humidity']; wind_5 = round(data['list'][32]['wind']['speed'], 1)
    
    await callback.message.edit_text(
          f"🌍 {html.italic(d.weather_indicators[0])} {html.bold(city.title())} {html.italic(d.weather_indicators[9])}\n\n\n"
          f"{html.italic(date_1)}\n🌡 {html.bold(d.weather_indicators[1])} {'+' if temp_1 >= 1.0 else ''}{temp_1} {d.code_to_smile[weather_1]if weather_1 in d.code_to_smile else ''}\n"
          f"💧 {html.bold(d.weather_indicators[2])} {humidity_1}%\n🍃 {html.bold(d.weather_indicators[4])} {wind_1} м/с\n\n"
          f"{html.italic(date_2)}\n🌡 {html.bold(d.weather_indicators[1])} {'+' if temp_2 >= 1.0 else ''}{temp_2} {d.code_to_smile[weather_2]if weather_2 in d.code_to_smile else ''}\n"
          f"💧 {html.bold(d.weather_indicators[2])} {humidity_2}%\n🍃 {html.bold(d.weather_indicators[4])} {wind_2} м/с\n\n"
          f"{html.italic(date_3)}\n🌡 {html.bold(d.weather_indicators[1])} {'+' if temp_3 >= 1.0 else ''}{temp_3} {d.code_to_smile[weather_3]if weather_3 in d.code_to_smile else ''}\n"
          f"💧 {html.bold(d.weather_indicators[2])} {humidity_3}%\n🍃 {html.bold(d.weather_indicators[4])} {wind_3} м/с\n\n"
          f"{html.italic(date_4)}\n🌡 {html.bold(d.weather_indicators[1])} {'+' if temp_4 >= 1.0 else ''}{temp_4} {d.code_to_smile[weather_4]if weather_4 in d.code_to_smile else ''}\n"
          f"💧 {html.bold(d.weather_indicators[2])} {humidity_4}%\n🍃 {html.bold(d.weather_indicators[4])} {wind_4} м/с\n\n"
          f"{html.italic(date_5)}\n🌡 {html.bold(d.weather_indicators[1])} {'+' if temp_5 >= 1.0 else ''}{temp_5} {d.code_to_smile[weather_5]if weather_5 in d.code_to_smile else ''}\n"
          f"💧 {html.bold(d.weather_indicators[2])} {humidity_5}%\n🍃 {html.bold(d.weather_indicators[4])} {wind_5} м/с"
          )
    
"""Вывод информации о профиле пользователя"""
async def output_profil_data(message: Message, city_name):
    await message.answer(
        f"ℹ️ {html.italic(d.profil_settings[0])}\n\n"
        f"🏙️ {d.profil_settings[1]} {html.bold(city_name)}",
        
        reply_markup=kb.profile_settings
    )
