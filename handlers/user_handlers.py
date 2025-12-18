from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from database.users_db import get_user, is_registered
from keyboards.reply import main_menu
from keyboards.inline import profile_kb

router = Router()

@router.message(CommandStart())
async def start_message(message: Message):
    user_id = message.from_user.id
    if await is_registered(user_id):
        await message.answer("Bosh sahifa", reply_markup=main_menu)
    else:
        await message.answer("Ismingizni kiriting:")

@router.message(F.text == "Profil👤")
async def profile(message: Message):
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("Birinchi registratsiya qilishingiz kerak")
        return

    first, last, phone_number = user

    # from database.events_db import get_registered_events, get_event_by_id
    from database.registrations_db import get_registered_events
    from database.events_db import get_event_by_id
    registered_raw = await get_registered_events(message.from_user.id)
    registered_ids = [r[0] if isinstance(r, (list, tuple)) else r for r in registered_raw]

    if not registered_ids:
        events_info = "Siz hali biron-bir tadbirga registratsiya qilmagansiz."
    else:
        lines = []
        for ev_id in registered_ids:
            ev = await get_event_by_id(ev_id)
            if not ev:
                continue
            lines.append(f"<b>📌Nomi:</b> {ev[1]}; ⏰Vaqti: {ev[3]};📍<a href='{ev[6]}'>Havola</a>")

        events_info = "\n".join(lines) if lines else "Siz hali biron-bir tadbirga registratsiya qilmagansiz."

    await message.answer(
        f"Ism: {first}\nFamiliya: {last}\nTelefon raqam: {phone_number}\n\nRegistratsiyadan o'tgan tadbirlar:\n{events_info}\n\n",
        reply_markup=profile_kb,
        disable_web_page_preview=True
    )

@router.message(Command("help"))
async def help_bot(message: Message):
    await message.answer("Savolingiz bulsa: @akramovaf\nBot bo'yicha takliflar: @simple_urm")
@router.message(F.text == "💳 Karta 1")
async def card1(message: Message):
    await message.answer("5614 6849 0286 4006 I.Sh")


@router.message(F.text == "💳 Karta 2")
async def card2(message: Message):
    await message.answer("4198 1300 1839 2711 I.Sh")


@router.message(F.text == "Admindan yordam")
async def admin_help(message: Message):
    await message.answer("@akramovaf")
