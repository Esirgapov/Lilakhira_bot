from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database.users_db import update_user, get_user

router = Router()

class Edit(StatesGroup):
    first = State()
    last = State()
    phone = State()


@router.callback_query(F.data == "change_first")
async def edit_first(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Edit.first)
    await callback.message.answer("Yangi ismni kiriting:")
    await callback.answer()


@router.callback_query(F.data == "change_last")
async def edit_last(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Edit.last)
    await callback.message.answer("Yangi familiyani kiriting:")
    await callback.answer()

@router.callback_query(F.data == "change_phone")
async def edit_phone(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Edit.phone)
    await callback.message.answer('Yangi Telefon raqamni kiriting:')
    await callback.answer()

@router.message(Edit.first)
async def save_new_first(message: Message, state: FSMContext):
    new_first = message.text
    user_id = message.from_user.id
    old = await get_user(user_id)
    await update_user(user_id, new_first, old[1], old[2])
    await state.clear()
    await message.answer("Ism o'zgartirildi")


@router.message(Edit.last)
async def save_new_last(message: Message, state: FSMContext):
    new_last = message.text
    user_id = message.from_user.id
    old = await get_user(user_id)
    await update_user(user_id, old[0], new_last, old[2])
    await state.clear()
    await message.answer("Familiya o'zgartirildi")

@router.message(Edit.phone)
async def save_new_phone(message: Message, state: FSMContext):
    new_phone = message.text
    user_id = message.from_user.id
    old = await get_user(user_id)
    await update_user(user_id, old[0], old[1], new_phone)
    await state.clear()
    await message.answer("Telefon raqam o'zgartirildi")