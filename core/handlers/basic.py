import json
from datetime import datetime

from aiogram import Bot
from aiogram.types import Message

from core.utils.dbconnect import Request
from core.keyboards.inline import first_reg_keyboard, add_player_keyboard, all_players_keyboard


async def get_start(message: Message, request: Request):
    if message.chat.type == 'private':
        await message.answer(f"Салам, {message.from_user.first_name}!"
                             f"\nЧтобы начать пользоваться ботом, надо его сначала в группу добавить")

    elif message.chat.type == 'group' or message.chat.type == 'supergroup':
        if not await request.check_group(message.chat.id):
            await request.add_group(
                group_chat_id=message.chat.id,
                group_name=message.chat.title
            )
            await message.answer(f"Красавчики,че. Добавили в первый раз в группу? "
                                 f"Значит надо зарегать всех кто будет играть.", reply_markup=first_reg_keyboard())
        else:
            await message.answer(
                f"Кто сегодня({datetime.now().date().strftime('%d.%m.%Y')}) чемпион?",
                reply_markup=await all_players_keyboard(request, message.chat.id)
            )


async def add_new_player(message: Message):
    await message.answer(
        f"Хорошо. Кнопку должен нажать тот, кого надо добавить.",
        reply_markup=add_player_keyboard()
    )


async def show_all_stats(message: Message, request: Request):
    all_stats = await request.get_all_stats(message.chat.id)
    answer = f"Статистика:"
    counter = 1
    for user_id, number in all_stats.items():
        player = await request.get_user(user_id)
        answer += f"\n{counter}. {player[0]['first_name']}: <b>{number}</b>"
        counter += 1
    await message.answer(answer)
