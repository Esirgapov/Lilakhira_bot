from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.events_db import get_events
from database.registrations_db import register_user
from aiogram.exceptions import TelegramBadRequest
import os


events_router = Router()

# Функция генерации клавиатуры с динамическими кнопками
def create_event_keyboard(index: int, total: int, event_id: int) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    row_buttons = []

    if index > 0:
        row_buttons.append(InlineKeyboardButton(text="⬅️", callback_data=f"ev_prev_{index-1}"))

    row_buttons.append(InlineKeyboardButton(text="Registratriya", callback_data=f"ev_reg_{event_id}"))

    if index < total - 1:
        row_buttons.append(InlineKeyboardButton(text="➡️", callback_data=f"ev_next_{index+1}"))

    kb_builder.row(*row_buttons)
    return kb_builder.as_markup()


async def format_event(ev):
    text = (
        f"<b>{ev[1]}</b>\n"
        f"📍 Manzil: {ev[2]}\n"
        f"⏰ Vaqti: {ev[3]}\n"
        f"🧭 Mo'ljal: {ev[4]}\n"
        f"🚇 Metro: {ev[5]}\n"
        f"🌐 <a href='{ev[6]}'>Havola</a>"
    )
    return text


async def update_event_message(call: CallbackQuery, ev, index: int, total: int):
    text = await format_event(ev)
    kb = create_event_keyboard(index, total, ev[0])
    image = ev[7] if len(ev) > 7 else None

    if image:
        try:
            await call.message.edit_media(media=InputMediaPhoto(media=image, caption=text), reply_markup=kb)
        except:
            await call.message.edit_caption(caption=text, reply_markup=kb)
    else:
        try:
            await call.message.edit_caption(caption=text, reply_markup=kb)
        except:
            await call.message.edit_text(text, reply_markup=kb)


# @events_router.message(F.text == "Jamoaviy hashar")
# async def events(message: Message):
#     events = await get_events()
#     if not events:
#         await message.answer("Jamoaviy hasharlar yo'q.")
#         return

#     ev = events[0]
#     txt = await format_event(ev)
#     kb = create_event_keyboard(0, len(events), ev[0])
#     image = ev[7] if len(ev) > 7 else None
#     if image:
#         await message.answer_photo(photo=image, caption=txt, reply_markup=kb)
#     else:
#         await message.answer(txt, reply_markup=kb)

@events_router.message(F.text == "Jamoaviy hashar")
async def events(message: Message):
    events = await get_events()
    if not events:
        await message.answer("Jamoaviy hasharlar yo'q.")
        return
    ev = events[0]
    txt = await format_event(ev)
    kb = create_event_keyboard(0, len(events), ev[0])
    image = ev[7] if len(ev) > 7 else None
    if not image:
        await message.answer(txt, reply_markup=kb)
        return
    try:
        if isinstance(image, str) and image.startswith("http"):
            await message.answer_photo(photo=image, caption=txt, reply_markup=kb)
        elif isinstance(image, str) and os.path.exists(image):
            await message.answer_photo(photo=FSInputFile(image), caption=txt, reply_markup=kb)
        else:
            await message.answer_photo(photo=image, caption=txt, reply_markup=kb)
    except TelegramBadRequest:
        await message.answer(
            "Неправильный формат изображения.\n"
            "Фото должно быть обычное (сжатое)."
        )

@events_router.callback_query(F.data.startswith("ev_prev_"))
async def prev_event(call: CallbackQuery):
    await call.answer()
    index = int(call.data.split("_")[-1])
    events = await get_events()
    ev = events[index]
    await update_event_message(call, ev, index, len(events))


@events_router.callback_query(F.data.startswith("ev_next_"))
async def next_event(call: CallbackQuery):
    await call.answer()
    index = int(call.data.split("_")[-1])
    events = await get_events()
    ev = events[index]
    await update_event_message(call, ev, index, len(events))



@events_router.callback_query(F.data.startswith("ev_reg_"))
async def register_event(call: CallbackQuery):
    try:
        event_id = int(call.data.split("_")[-1])
    except:
        await call.answer("Hatolik...", show_alert=True)
        return

    created = await register_user(call.from_user.id, event_id)
    if not created:
        await call.answer("Siz bu Tadbirga registratsiya qilib bo'lgansiz.", show_alert=True)
    else:
        await call.answer("Siz muvaffaqiyatli ro'yxatdan o'tdingiz.")
