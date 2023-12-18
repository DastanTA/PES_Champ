from aiogram import Bot
from aiogram.types import CallbackQuery

from core.utils.dbconnect import Request


async def register_new_player(call: CallbackQuery, request: Request):
    if not await request.check_user(call.from_user.id):
        new_player = call.from_user.first_name
        await request.add_user(user_id=call.from_user.id, first_name=new_player, group_chat_id=call.message.chat.id)
        await call.message.answer(f"Новый игрок <b>{new_player}</b> зарегистрирован.")
    else:
        await call.message.answer(f"Игрок <b>{call.from_user.first_name}</b> уже есть в базе.")

    await call.answer()


async def done_registering_players(call: CallbackQuery, bot: Bot):
    await call.message.answer(f"Отлично зарегистрировали всех. Но если кого-то забыли добавить, "
                              f"можете воспользоваться командой /add_player.\nЧтобы зарегать чемпиона "
                              f"выберите команду /start еще раз.")
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id, reply_markup=None)
    await call.answer()


async def add_new_player(call: CallbackQuery, request: Request, bot: Bot):
    counter = 0
    if not await request.check_user(call.from_user.id):
        new_player = call.from_user.first_name
        await request.add_user(user_id=call.from_user.id, first_name=new_player, group_chat_id=call.message.chat.id)
        await call.message.answer(f"Новый игрок <b>{new_player}</b> зарегистрирован.")
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id, reply_markup=None)
    else:
        await call.answer(f"Игрок <b>{call.from_user.first_name}</b> уже есть в базе.")
        # if counter == 4:
        #     await call.message.answer(f"<b>{call.from_user.first_name}</b>, заебал экенсиң го!.")
        #     counter = 0
        # else:
        #     await call.message.answer(f"Игрок <b>{call.from_user.first_name}</b> уже есть в базе.")
        #     counter += 1

    await call.answer()
