from config import DATABASE_NAME
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import html
import keyboards as kb
from db import DataBase
import get_weather_data as getdata
import output_data as outputdata

router = Router()

class Weather(StatesGroup): # Машина состояний
    city = State()
    city_locate = State()

"""Обработка команды старт"""
@router.message(CommandStart())
async def cmd_start(message: Message):
    db = DataBase(DATABASE_NAME)
    
    if(db.check_user(message.from_user.id) == None):
        db.add_user(message.from_user.id)
    
        await message.answer(f"🔥 Привет {html.bold(html.quote(message.from_user.full_name))}, выберите доступное действие на панели управления.", 
                            reply_markup=kb.main)
    else:
        await message.answer(f"📢 {html.bold(html.quote(message.from_user.full_name))}, выберите доступное действие.", reply_markup=kb.main)

"""Обработка погоды по ручному глобальному поиску"""
@router.message(F.text == "⛅ Погода - В мире 🌍")
async def get_weather_world(message: Message, state: FSMContext):
    await message.answer(f"📝 Введите название населеного пункта.\n\nЧтобы выйти из режима поиска, нажмите - Отмена", reply_markup=kb.cancel)
    await state.set_state(Weather.city)

@router.message(Weather.city)
async def get_weather_city(message: Message, state: FSMContext): 
    try:
        await state.update_data(city=message.text)
        data_about_city = await state.get_data()
        city = data_about_city['city']
        
        if city == "❎ Отмена" or city == "/menu":
            await message.answer("🚬🗿 Выберите пункт меню.", reply_markup=kb.main)
            await state.clear()
        else: 
            weather_res_status, weather_data = await getdata.get_weather_in_city(city)
            
            if weather_res_status==200:
                await outputdata.output_weather(message, weather_data, city)
            elif weather_res_status==404:
                await message.answer("❗ Неверное название города", reply_markup=kb.cancel)
    except:
        await message.answer(f"😠 Нет, так не пойдет, мне нужно название населенного пункта текстом")
        
"""Обработка погоды в городе пользователя"""
@router.message(F.text == "🌤️ Погода - Мой город 🏙️")
async def locat(message: Message):
    db = DataBase(DATABASE_NAME)
    user_city = db.check_city(message.from_user.id)
    
    if(user_city == None):
        await message.answer(f"👇 Выберите доступный способ для сохранения информации об вашем населенном пункте.", reply_markup=kb.send_locate)
    else:
        res, weather_data = await getdata.get_weather_in_city(user_city)
        await outputdata.output_weather(message, weather_data, user_city)
        await message.answer(f"ℹ️ Дополнительная информация о прогнозе погоды в населеном пункте {html.bold(user_city)}", reply_markup=kb.weather_five_day)

"""Обработка ручного ввода города пользователя"""
@router.message(F.text == "🖋️ Ввести вручную")
async def write(message: Message, state: FSMContext): 
    await message.answer("📝 Введите название населеного пункта.", reply_markup=kb.return_to_back)
    await state.set_state(Weather.city_locate)
    
@router.message(Weather.city_locate) 
async def get_weather_locate(message: Message, state: FSMContext): # Обработка введенных пользователем сообщений
    try:
        await state.update_data(city_locate=message.text)
        data_about_city = await state.get_data()
        city_name = data_about_city['city_locate']
        
        db = DataBase(DATABASE_NAME)
        
        if city_name == "⬇ Вернуться обратно":
            await state.clear()
            await message.answer("🚬🗿 Выберите действие.", reply_markup=kb.send_locate)
        elif city_name == "/menu":
            await state.clear()
            await message.answer("🚬🗿 Выберите пункт меню.", reply_markup=kb.main)
        else: 
            weather_res_status, weather_data = await getdata.get_weather_in_city(city_name)
            
            if weather_res_status==200:
                db.add_city(city_name, message.from_user.id)
                await message.answer(f"🏢 Населенный пункт - {html.bold(city_name.title())}, был успешно сохранен", reply_markup=kb.main)
                await state.clear()
            elif weather_res_status==404:
                await message.answer("❗ Неверное название населенного пункта", reply_markup=kb.return_to_back)
    except:
        await message.answer(f"😠 Нет, так не пойдет, мне нужно название населенного пункта текстом")

@router.message(F.location)
async def location(message: Message): # Получение геопозиции пользователя и сохранение в бд при успешной обработке
        
    lat = message.location.latitude
    lon = message.location.longitude
    
    weather_data = await getdata.get_coordinates_city(lat, lon)
    
    if weather_data['name'] == '':
        await message.answer("❗ Произошла ошибка, не удалось определить геопозицию, попробуйте снова.")
    else:
        global global_city 
        global_city = weather_data['name']
        
        await message.answer(f"🌏 Ваше местоположение {global_city}?", reply_markup=kb.confirm_locate)

# Обработка коллбэков для подтверждения действий пользователя
@router.callback_query(F.data == 'confirm') 
async def locat_confirm(callback: CallbackQuery):
    db = DataBase(DATABASE_NAME)
    db.add_city(global_city, callback.from_user.id)
    
    await callback.message.edit_text(f"✅ Местоположение успешно сохранено.")
    await callback.message.answer('🚬🗿 Выберите действие.', reply_markup=kb.main)

    
@router.callback_query(F.data == 'revoke')
async def locat_revoke(callback: CallbackQuery):
    await callback.message.edit_text(f"❗ Попробуйте снова.")

# Обработка коллбэка погоды на 5 дней
@router.callback_query(F.data == 'five_day')
async def weather_five_day(callback: CallbackQuery):
    db = DataBase(DATABASE_NAME)
    user_city = db.check_city(callback.from_user.id)
    
    weather_data = await getdata.get_weather_five_days(user_city)
    await outputdata.output_weather_five_days(callback, weather_data, user_city)
    
"""Обработка настройки профиля пользователя"""
@router.message(F.text == "⚙️ Настройки профиля")
async def profil(message: Message):
    db = DataBase(DATABASE_NAME)
    city_data = db.check_city(message.from_user.id)
    
    if(city_data == None):
        city_data = "Данные отсутствуют"
    
    await outputdata.output_profil_data(message, city_data)
        
@router.message(F.text == "✏️ Изменить данные")
async def change_info(message: Message):
    await message.answer(f"👇 Выберите доступный способ для изменения информации об вашем населенном пункте.", reply_markup=kb.send_locate)
    
@router.message(F.text == "✂️ Удалить данные")
async def delete_info(message: Message):
    db = DataBase(DATABASE_NAME)
    
    if(db.check_city(message.from_user.id) == None):
        await message.answer("❗ Информация о населенном пункте отсутствует.", reply_markup=kb.main)
    else: 
        await message.answer(f"❗ Вы действительно хотите удалить информацию о вашем населенном пункте?", reply_markup=kb.choise)

# Обработка коллбэков для подтверждения действий пользователя
@router.callback_query(F.data == 'choise_yes')
async def choise_yes(callback: CallbackQuery):
    db = DataBase(DATABASE_NAME)
    city = db.check_city(callback.from_user.id)
    db.delete_city(city, callback.from_user.id)
    
    await callback.message.edit_text(f"✅ Информация успешно удалена.")
    await callback.message.answer("🚬🗿 Выберите действие.", reply_markup=kb.main)
    
@router.callback_query(F.data == 'choise_no')
async def choise_no(callback: CallbackQuery):
    await callback.message.edit_text("✅ Операция отменена.")
    await callback.message.answer("🚬🗿 Выберите действие.", reply_markup=kb.main)
    
"""Обработка кнопки возрата в меню"""
@router.message(F.text == "🔄 Вернуться в меню")
async def back_to_menu(message: Message):
    await message.answer("🚬🗿 Выберите действие.", reply_markup=kb.main)   

"""Обработка кнопки 'О боте'"""
@router.message(F.text == "🤖 О боте")
async def bot_info(message: Message):
    await message.answer(f"📄 Информация о боте.\n\nВерсия 0.0.1\n\nРазработчик бота - @chonjone")
    
"""Обработка команды меню"""
@router.message(Command('menu'))
async def cmd_menu(message: Message):
    await message.answer(f"⚡ {html.bold(html.quote(message.from_user.full_name))}, выберите функцию из предложенного списка.", reply_markup=kb.main)

"""Обработка сообщений не подходящих под другие роутеры"""
@router.message()
async def cmd_other(message: Message):
    await message.answer(f"🌞 {html.bold(html.quote(message.from_user.full_name))}, напишите /menu если у вас нет панели управления или выберите действие.")
    