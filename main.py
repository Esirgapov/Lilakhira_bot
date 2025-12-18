import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config_data.config import Config, load_config

from handlers import user_handlers
from handlers import registration_handlers
from handlers import profile_edit
from handlers.events_admin import admin_router
from handlers.events_user import events_router

from database.db import init_db, create_db

logger = logging.getLogger(__name__)

async def main():
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format='%(filename)s:%(lineno)d #%(levelname)-8s '
    #            '[%(asctime)s] - %(name)s - %(message)s')
    # logger.info('Starting bot')

    # создаём таблицы, если нужно
    await create_db()   # db.sqlite3 -> users
    await init_db()     # events.db -> events, registrations

    config: Config = load_config()
    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()

    dp.include_router(registration_handlers.router)
    dp.include_router(profile_edit.router)
    dp.include_router(user_handlers.router)

    dp.include_router(admin_router)
    dp.include_router(events_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



