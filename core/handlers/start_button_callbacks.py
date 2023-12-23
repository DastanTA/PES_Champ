from aiogram.types import CallbackQuery

from core.utils.dbconnect import Request
from core.handlers.basic import (add_result_command, show_all_stats, show_all_stats_in_cups, show_this_year_stats,
                                 add_new_player, show_all_players, get_help)


async def add_result_button_callback(call: CallbackQuery, request: Request):
    await add_result_command(request=request, message=call.message)
    await call.answer()


async def all_stats_button_callback(call: CallbackQuery, request: Request):
    await show_all_stats(call.message, request)
    await call.answer()


async def all_stats_in_cups_button_callback(call: CallbackQuery, request: Request):
    await show_all_stats_in_cups(call.message, request)
    await call.answer()


async def this_year_stats_button_callback(call: CallbackQuery, request: Request):
    await show_this_year_stats(call.message, request)
    await call.answer()


async def add_player_button_callback(call: CallbackQuery):
    await add_new_player(call.message)
    await call.answer()


async def show_all_players_button_callback(call: CallbackQuery, request: Request):
    await show_all_players(call.message, request)
    await call.answer()


async def get_help_button_callback(call: CallbackQuery):
    await get_help(call.message)
    await call.answer()
