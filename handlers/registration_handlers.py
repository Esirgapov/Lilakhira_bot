from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart

from database.users_db import add_user, is_registered
from keyboards.reply import main_menu

router = Router()

class Reg(StatesGroup):
    first_name = State()
    last_name = State()
    phone = State()


@router.message(CommandStart())
async def start_reg(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if await is_registered(user_id):
        await message.answer("Bosh sahifa", reply_markup=main_menu)
    else:
        await state.set_state(Reg.first_name)
        await message.answer("Ismingizni kiriting:")


@router.message(Reg.first_name)
async def reg_first(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(Reg.last_name)
    await message.answer("Familiyangizni kiriting:")


@router.message(Reg.last_name)
async def reg_last(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await state.set_state(Reg.phone)
    await message.answer("Telefon raqamingizni kiriting:")

@router.message(Reg.phone)
async def reg_phonne(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    user_id = message.from_user.id

    await add_user(
        user_id,
        data["first_name"],
        data['last_name'],
        data['phone']        
    )
    await state.clear()
    await message.answer("Registratsiya yakunlandi", reply_markup=main_menu)