import asyncio
import logging
import asyncpg

from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.filters import Command

from config import BOT_TOKEN, ADMIN_ID, PGPORT, PGUSER, PGPASSWORD, HOST, DATABASE
from core.filters.iscontact import IsTrueContact
from core.handlers.basic import get_start, add_new_player
from core.handlers.contact import get_fake_contact, get_true_contact
from core.handlers.callback import register_new_player, done_registering_players, add_new_player_inline
from core.middlewares.dbmiddleware import DbSession
from core.utils.commands import set_commands


async def start_bot(bot: Bot):
    await set_commands(bot)
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

    dp.callback_query.register(register_new_player, F.data == 'new_player')
    dp.callback_query.register(done_registering_players, F.data == 'all_players_are_registered')
    dp.callback_query.register(add_new_player_inline, F.data == 'add_new_player')
    dp.message.register(get_start, Command(commands=["start"]))
    dp.message.register(add_new_player, Command(commands=["add_player"]))
    dp.message.register(get_true_contact, F.content_type == 'contact', IsTrueContact())
    dp.message.register(get_fake_contact, F.content_type == 'contact')

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
