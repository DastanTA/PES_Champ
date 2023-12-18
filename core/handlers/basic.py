import json

from aiogram import Bot
from aiogram.types import Message

from core.utils.dbconnect import Request
from core.keyboards.inline import first_reg_keyboard, add_player_keyboard


async def get_start(message: Message, request: Request):
    if message.chat.type == 'private':
        await message.answer(f"Салам, {message.from_user.first_name}!"
                             f"\nБотту колдонуп башташ үчүн биринчи группага кошуш керек")

    elif message.chat.type == 'group' or message.chat.type == 'supergroup':
        if not await request.check_group(message.chat.id):
            await request.add_group(
                group_chat_id=message.chat.id,
                group_name=message.chat.title
            )
            await message.answer(f"Красавчики,че. Добавили в первый раз в группу? "
                                 f"Значит надо зарегать всех кто будет играть.", reply_markup=first_reg_keyboard())


async def add_new_player(message: Message):
    await message.answer(
        f"Хорошо. Кнопку должен нажать тот, кого надо добавить.",
        reply_markup=add_player_keyboard()
    )
