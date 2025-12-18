from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Profil👤')],
        [KeyboardButton(text='💳 Karta 1'), KeyboardButton(text='💳 Karta 2')],
        [KeyboardButton(text='Admindan yordam'), KeyboardButton(text='Jamoaviy hashar')]
    ],
    resize_keyboard=True
)
