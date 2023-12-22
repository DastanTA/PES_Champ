from datetime import datetime
from collections import Counter

from aiogram import Bot
from aiogram.types import CallbackQuery

from core.utils.dbconnect import Request
from core.handlers.basic import _get_stats_str
from core.handlers import basic


async def register_new_player(call: CallbackQuery, request: Request):
    if not await request.check_user(call.from_user.id, call.message.chat.id, call.from_user.first_name):
        new_player = call.from_user.first_name
        await request.add_user(user_id=call.from_user.id, first_name=new_player, group_chat_id=call.message.chat.id)
        await call.message.answer(f"Новый игрок <b>{new_player}</b> зарегистрирован.")
    else:
        await call.answer(f"Игрок {call.from_user.first_name} уже есть в базе.", show_alert=True)

    await call.answer()


async def done_registering_players(call: CallbackQuery, bot: Bot, request: Request):
    all_users = await request.all_users(call.message.chat.id)
    answer_str = (f"Отлично зарегистрировали всех. Но если кого-то забыли добавить, "
                  f"можете воспользоваться командой /add_player.\nЧтобы зарегать "
                  f"чемпиона выберите команду /start еще раз. Кого зарегистрировали:")
    for user in all_users:
        answer_str += f"\n<b>{user['first_name']}</b>"
    await call.message.answer(answer_str)
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id, reply_markup=None)
    await call.answer()


async def add_new_player_inline(call: CallbackQuery, request: Request, bot: Bot):
    if not await request.check_user(call.from_user.id, call.message.chat.id, call.from_user.first_name):
        new_player = call.from_user.first_name
        await request.add_user(user_id=call.from_user.id, first_name=new_player, group_chat_id=call.message.chat.id)
        await call.message.answer(f"Новый игрок <b>{new_player}</b> зарегистрирован.")
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id, reply_markup=None)
    else:
        await call.answer(f"Игрок {call.from_user.first_name} уже есть в базе.", show_alert=True)

    await call.answer()


async def add_champ_result(call: CallbackQuery, request: Request, bot: Bot):
    user_id = int(call.data.split("_")[1])
    winner = await request.get_user(user_id)

    if user_id != call.from_user.id:
        if await request.check_user(call.from_user.id, call.message.chat.id, call.from_user.first_name):
            if call.from_user.id not in basic.votes[call.message.chat.id].keys():
                basic.votes[call.message.chat.id][call.from_user.id] = user_id
                await call.message.answer(f"{call.from_user.first_name} проголосовал за {winner[0]['first_name']}")
            else:
                await call.answer(f"Вы уже голосовали!")
        else:
            await call.answer(f"{call.from_user.first_name}, вы не можете голосовать. Вы не зарегистрованы. "
                              f"Чтобы зарегаться вызовите команду /add_player", show_alert=True)
    else:
        await call.answer(f"{winner[0]['first_name']}, вы не можете голосовать за себя")

    counted_votes = dict(Counter(basic.votes[call.message.chat.id].values()))
    for _, value in basic.votes[call.message.chat.id].items():
        if counted_votes[value] >= 2:
            await request.add_champion(call.message.chat.id, winner[0]["user_id"])
            this_year = await request.get_stats_current_year(call.message.chat.id)
            stats = await _get_stats_str(request, this_year, answer=f"Статистика текущего года:\n")
            answer = (f"Сегодня[{datetime.now().date().strftime('%d.%m.%Y')}] "
                      f"чемпион: <b>{winner[0]['first_name']}</b>\n\n{stats}")
            await call.message.answer(answer)
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                message_id=call.message.message_id, reply_markup=None)
            basic.votes[call.message.chat.id] = {}
            break
        else:
            continue

    await call.answer()


async def cancel_champ_process(call: CallbackQuery, bot: Bot):
    basic.votes[call.message.chat.id] = {}
    await call.message.answer("Процесс регистрации чемпиона отменен. Нажмите на /start, если хотите начать заново.")
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id, reply_markup=None)


async def delete_last_record(call: CallbackQuery, request: Request, bot: Bot):
    if call.data == "delete_no":
        await call.answer("Удаление последней записи отменена.")
        await call.message.delete()
    elif call.data == "delete_yes":
        await request.delete_last_record_champ_result(call.message.chat.id)
        all_stats = await request.get_all_stats(call.message.chat.id)
        stats = await _get_stats_str(request, all_stats, answer=f"Статистика за все время:\n")
        answer = f"Последняя запись с базы удалена.\n\n{stats}"
        await call.message.answer(answer)
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id, reply_markup=None)
        await call.answer()
