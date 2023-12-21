from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message

from core.utils.dbconnect import Request


def first_reg_keyboard():
    inline_keyboard = InlineKeyboardBuilder()
    inline_keyboard.button(text="Я участвую!", callback_data="new_player")
    inline_keyboard.button(text="Готово", callback_data="all_players_are_registered")
    inline_keyboard.adjust(2)
    return inline_keyboard.as_markup()


def add_player_keyboard():
    inline_keyboard = InlineKeyboardBuilder()
    inline_keyboard.button(text="Добавить меня", callback_data="add_new_player")
    return inline_keyboard.as_markup()


async def all_players_keyboard(request: Request, chat_id: int):
    inline_keyboard = InlineKeyboardBuilder()

    all_players = await request.all_users(chat_id)
    for player in all_players:
        inline_keyboard.button(text=f"{player['first_name']}", callback_data=f"champ_{player['user_id']}")
    inline_keyboard.button(text=f"отмена", callback_data=f"cancel_record_process")
    return inline_keyboard.as_markup()
