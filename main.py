import asyncio
import logging
import asyncpg

from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.filters import Command

from config import BOT_TOKEN, ADMIN_ID, PGPORT, PGUSER, PGPASSWORD, HOST, DATABASE
from core.filters.iscontact import IsTrueContact
from core.handlers.basic import get_start
from core.handlers.contact import get_fake_contact, get_true_contact
from core.middlewares.dbmiddleware import DbSession


async def start_bot(bot: Bot):
    await bot.send_message(ADMIN_ID, "Бот запущен.")


async def stop_bot(bot: Bot):
    await bot.send_message(ADMIN_ID, "Бот остановлен.")


async def create_pool():
    return await asyncpg.create_pool(user=PGUSER, password=PGPASSWORD, host=HOST,
                                     database=DATABASE, port=PGPORT, command_timeout=60)


async def start():
    logging.basicConfig(level=logging.INFO, filename="all_logs.log",
                        format="%(asctime)s - [%(levelname)s] -  %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    pool_connect = await create_pool()

    dp = Dispatcher()
    dp.update.middleware.register(DbSession(pool_connect))
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(get_start, Command(commands=["start"]))
    dp.message.register(get_true_contact, F.content_type.CONTACT, IsTrueContact())
    dp.message.register(get_fake_contact, F.content_type.CONTACT)

    try:
        # await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
