from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, ReplyKeyboardMarkup, KeyboardButton, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from database.events_db import get_events, add_event, delete_event, get_event_by_id
from handlers.user_handlers import start_message
from aiosqlite import connect

ADMIN_ID = 8096637274
admin_router = Router()


class AddEventFSM(StatesGroup):
    name = State()
    location = State()
    time = State()
    orientir = State()
    metro = State()
    link = State()
    image = State()


@admin_router.message(F.text == "/admin")
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Добавить ивент"), KeyboardButton(text="Удалить ивент")],
            [KeyboardButton(text="Главное меню"), KeyboardButton(text="Ивенты")]
        ],
        resize_keyboard=True
    )
    await message.answer("Админ панель:", reply_markup=kb)


@admin_router.message(F.text == "Добавить ивент")
async def add_event_start(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    await state.set_state(AddEventFSM.name)
    await message.answer("Имя ивента:")

@admin_router.message(F.text == "Главное меню")
async def add_event_start(message: Message):
    return await start_message(message)

# 
@admin_router.message(F.text == "Удалить ивент")
async def delete_event_start(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    events = await get_events()
    if not events:
        await message.answer("Ивентов нет.")
        return
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=ev[1], callback_data=f"del_ev_{ev[0]}")] for ev in events
        ]
    )
    await message.answer("Выберите ивент для удаления:", reply_markup=kb)

@admin_router.message(F.text == "Ивенты")
async def events_admin(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    events = await get_events()
    if not events:
        await message.answer("Ивентов нет.")
        return
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=ev[1], callback_data=f"events_ev_{ev[0]}")] for ev in events
        ]
    )
    await message.answer("Выберите ивент:", reply_markup=kb)

@admin_router.callback_query(F.data.startswith("del_ev_"))
async def delete_event_callback(call: CallbackQuery):
    event_id = int(call.data.split("_")[-1])
    await delete_event(event_id)
    await call.message.edit_text("Ивент удалён.")

@admin_router.callback_query(F.data.startswith("events_ev_"))
async def event_details_callback(call: CallbackQuery):
    event_id = int(call.data.split("_")[-1])
    events = await get_events()
    ev = next((e for e in events if e[0] == event_id), None)
    if not ev:
        await call.answer("Ивент не найден.", show_alert=True)
        return
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Участники", callback_data=f"registered_users_list_{ev[0]}")]
        ]
    )
    text = (
        f"<b>{ev[1]}</b>\n\n"
        f"<b>Место:</b> {ev[2]}\n"
        f"<b>Вакти:</b> {ev[3]}\n"
        f"<b>Молжал:</b> {ev[4]}\n"
        f"<b>Метро:</b> {ev[5]}\n"
        f"<b>Ссылка Локаций:</b> {ev[6]}"
    )
    image = ev[7] if len(ev) > 7 else None
    if image:
        await call.answer()
        await call.message.answer_photo(photo=image, caption=text, reply_markup=kb)
    else:
        await call.answer()
        await call.message.answer(text, reply_markup=kb)

@admin_router.callback_query(F.data.startswith("registered_users_list_"))
async def registered_users_list_callback(call: CallbackQuery):
    event_id = int(call.data.split("_")[-1])

    async with connect("database.db") as reg_db:
        cursor = await reg_db.execute(
            "SELECT user_id FROM registrations WHERE event_id = ?",
            (event_id,)
        )
        rows = await cursor.fetchall()

    if not rows:
        await call.answer("Участников нет.", show_alert=True)
        return

    user_ids = [row[0] for row in rows]

    names = []

    for uid in user_ids:
        async with connect("database.db") as user_db:
            cur = await user_db.execute(
                "SELECT first_name, last_name, phone FROM users WHERE user_id = ?",
                (uid,)
            )
            user = await cur.fetchone()

        if user:
            full_name = f"{user[0]} {user[1]} {user[2]}"
        else:
            full_name = f"User {uid}"

        names.append(full_name)

    event = await get_event_by_id(event_id)
    event_name = event[1] if event else "Ивент"

    text = f"Список участников на ивент «{event_name}»:\n\n"
    for i, name in enumerate(names, start=1):
        text += f"{i}) {name}\n"
    await call.answer()
    await call.message.answer(text)

@admin_router.message(AddEventFSM.name)
async def event_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddEventFSM.location)
    await message.answer("Манзил:")


@admin_router.message(AddEventFSM.location)
async def event_location(message: Message, state: FSMContext):
    await state.update_data(location=message.text)
    await state.set_state(AddEventFSM.time)
    await message.answer("Вакти:")

@admin_router.message(AddEventFSM.time)
async def event_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await state.set_state(AddEventFSM.orientir)
    await message.answer("Молжал:")


@admin_router.message(AddEventFSM.orientir)
async def event_orientir(message: Message, state: FSMContext):
    await state.update_data(orientir=message.text)
    await state.set_state(AddEventFSM.metro)
    await message.answer("Энг якин метро:")


@admin_router.message(AddEventFSM.metro)
async def event_metro(message: Message, state: FSMContext):
    await state.update_data(metro=message.text)
    await state.set_state(AddEventFSM.link)
    await message.answer("Location (ссылка):")


@admin_router.message(AddEventFSM.link)
async def event_link(message: Message, state: FSMContext):
    await state.update_data(link=message.text)
    await message.answer("Теперь отправьте картинку для ивента:")
    await state.set_state(AddEventFSM.image)


@admin_router.message(AddEventFSM.image, F.photo)
async def event_image(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(image=photo_id)

    data = await state.get_data()

    await add_event(
        data["name"],
        data["location"],
        data["time"],
        data["orientir"],
        data["metro"],
        data["link"],
        data["image"]
    )
    await message.answer("Ивент добавлен.")
    await state.clear()


@admin_router.message(F.text == "Удалить ивент")
async def delete_event_start(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    events = await get_events()
    if not events:
        await message.answer("Ивентов нет.")
        return
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=ev[1], callback_data=f"del_ev_{ev[0]}")] for ev in events]
    )
    await message.answer("Выберите ивент для удаления:", reply_markup=kb)

@admin_router.callback_query(F.data.startswith("del_ev_"))
async def delete_event_callback(call: CallbackQuery):
    event_id = int(call.data.split("_")[-1])
    await delete_event(event_id)
    await call.message.edit_text("Ивент удалён.")
    await call.answer()


