from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

profile_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ismni o'zgartirish", callback_data="change_first")],
        [InlineKeyboardButton(text="Familiyani o'zgartirish", callback_data="change_last")],
        [InlineKeyboardButton(text="Telefon raqamni o'zgartirish", callback_data="change_phone")]
    ]
)
