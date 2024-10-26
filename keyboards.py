from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="🌤️ Погода - Мой город 🏙️")],
    [KeyboardButton(text="⛅ Погода - В мире 🌍")],
    [KeyboardButton(text="⚙️ Настройки профиля")],
    [KeyboardButton(text="🤖 О боте")]
],
                           resize_keyboard=True,
                           input_field_placeholder="Выберите пункт меню.")

send_locate = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📌 Отправить геопозицию", request_location=True)],
    [KeyboardButton(text="🖋️ Ввести вручную")],
    [KeyboardButton(text="🔄 Вернуться в меню")]
],
                            resize_keyboard=True,
                            input_field_placeholder="Выберите пункт меню...")

profile_settings = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="✏️ Изменить данные")],
    [KeyboardButton(text="✂️ Удалить данные")],
    [KeyboardButton(text="🔄 Вернуться в меню")]
],
                            resize_keyboard=True,
                            input_field_placeholder="Выберите пункт меню...")

cancel = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="❎ Отмена")],
],
                           resize_keyboard=True,
                           input_field_placeholder="Выберите пункт меню...")

return_to_back = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="⬇ Вернуться обратно")]
],
                            resize_keyboard=True,
                            input_field_placeholder="Выберите пункт меню...")

confirm_locate = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Да, верно", callback_data='confirm')],
    [InlineKeyboardButton(text="❌ Нет, неверно", callback_data='revoke')]
])

choise = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Да, хочу", callback_data='choise_yes'),
    InlineKeyboardButton(text="❌ Нет, не хочу", callback_data='choise_no')]
])

weather_five_day = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🌦️ Прогноз погоды на 5 дней", callback_data='five_day')],
])