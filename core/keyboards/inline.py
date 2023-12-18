from aiogram.utils.keyboard import InlineKeyboardBuilder


def first_reg_keyboard():
    inline_keyboard = InlineKeyboardBuilder()
    inline_keyboard.button(text="Я участвую!", callback_data="new_player")
    inline_keyboard.button(text="Готово", callback_data="all_players_are_registered")
    inline_keyboard.adjust(2)
    return inline_keyboard.as_markup()
