import asyncio
import logging
import asyncpg

from aiogram import Bot, Dispatcher
from aiogram import F
from aiogram.filters import Command

from config import BOT_TOKEN, ADMIN_ID, PGPORT, PGUSER, PGPASSWORD, HOST, DATABASE
from core.handlers.basic import (get_start, add_result_command, add_new_player, show_all_stats, show_this_year_stats,
                                 cancel_last_record, show_all_stats_in_cups, show_all_players, get_help)
from core.handlers.callback import (register_new_player, done_registering_players, add_new_player_inline,
                                    add_champ_result, cancel_champ_process, delete_last_record)
from core.handlers.start_button_callbacks import (
    add_result_button_callback, all_stats_button_callback, all_stats_in_cups_button_callback,
    this_year_stats_button_callback, add_player_button_callback, show_all_players_button_callback,
    get_help_button_callback)
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
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] -  %(name)s - "
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
    dp.callback_query.register(add_champ_result, F.data.startswith('champ_'))
    dp.callback_query.register(cancel_champ_process, F.data == 'cancel_record_process')
    dp.callback_query.register(delete_last_record, F.data.startswith('delete_'))
    dp.callback_query.register(add_result_button_callback, F.data == 'add_champ')
    dp.callback_query.register(all_stats_button_callback, F.data == 'all_stats')
    dp.callback_query.register(all_stats_in_cups_button_callback, F.data == 'all_stats_in_cups')
    dp.callback_query.register(this_year_stats_button_callback, F.data == 'this_year_stats')
    dp.callback_query.register(add_player_button_callback, F.data == 'add_player_button')
    dp.callback_query.register(show_all_players_button_callback, F.data == 'all_players_button')
    dp.callback_query.register(get_help_button_callback, F.data == 'help_instructions')

    dp.message.register(get_start, Command(commands=["start"]))
    dp.message.register(add_result_command, Command(commands=["add_result"]))
    dp.message.register(add_new_player, Command(commands=["add_player"]))
    dp.message.register(show_all_players, Command(commands=["all_players"]))
    dp.message.register(show_all_stats, Command(commands=["all_stats"]))
    dp.message.register(show_all_stats_in_cups, Command(commands=["all_stats_in_cups"]))
    dp.message.register(show_this_year_stats, Command(commands=["this_year_stats"]))
    dp.message.register(cancel_last_record, Command(commands=["cancel"]))
    dp.message.register(get_help, Command(commands=["help"]))

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
