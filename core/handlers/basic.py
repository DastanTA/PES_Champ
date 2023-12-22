from datetime import datetime

from aiogram.types import Message

from core.utils.dbconnect import Request
from core.keyboards.inline import first_reg_keyboard, add_player_keyboard, all_players_keyboard, yes_no_keyboard


votes = dict()


async def get_start(message: Message, request: Request):
    if message.chat.type == 'private':
        await message.answer(f"Салам, {message.from_user.first_name}!"
                             f"\nЧтобы начать пользоваться ботом, надо его сначала в группу добавить")

    elif message.chat.type == 'group' or message.chat.type == 'supergroup':
        if not await request.check_group(message.chat.id, message.chat.title):
            await request.add_group(
                group_chat_id=message.chat.id,
                group_name=message.chat.title
            )
            await message.answer(f"Красавчики,че. Добавили в первый раз в группу? "
                                 f"Значит надо зарегать всех кто будет играть.", reply_markup=first_reg_keyboard())
        else:
            votes[message.chat.id] = {}
            await message.answer(
                f"Кто сегодня({datetime.now().date().strftime('%d.%m.%Y')}) чемпион?"
                f"\nКроме самого чемпиона, минимум двое должны проголосовать за него.",
                reply_markup=await all_players_keyboard(request, message.chat.id)
            )


async def add_new_player(message: Message):
    await message.answer(
        f"Хорошо. Кнопку должен нажать тот, кого надо добавить.",
        reply_markup=add_player_keyboard()
    )


async def get_stats_str(request: Request, query_result: dict, answer: str) -> str:
    counter = 1
    for user_id, number in query_result.items():
        player = await request.get_user(user_id)
        answer += f"\n{counter}. {player[0]['first_name']}: <b>{number}</b>"
        counter += 1
    return answer


async def turn_num_to_cups(number: int) -> str:
    cups = ""
    for i in range(1, number + 1):
        cups += "🏆"
    return cups


async def get_stats_in_cups(request: Request, query_result: dict, answer: str) -> str:
    counter = 1
    for user_id, number in query_result.items():
        player = await request.get_user(user_id)
        answer += f"\n{counter}. {player[0]['first_name']}: <b>{await turn_num_to_cups(number)}</b>"
        counter += 1
    return answer


async def show_all_stats(message: Message, request: Request):
    all_stats = await request.get_all_stats(message.chat.id)
    answer = await get_stats_str(request, all_stats, answer=f"Общая статистика:\n")
    await message.answer(answer)


async def show_all_stats_in_cups(message: Message, request: Request):
    all_stats = await request.get_all_stats(message.chat.id)
    answer = await get_stats_in_cups(request, all_stats, answer=f"Общая статистика:\n")
    await message.answer(answer)


async def show_this_year_stats(message: Message, request: Request):
    this_year = await request.get_stats_current_year(message.chat.id)
    answer = await get_stats_str(request, this_year, answer=f"Статистика текущего года:\n")
    await message.answer(answer)


async def cancel_last_record(message: Message, request: Request):
    if not await request.get_any_record(message.chat.id):
        await message.answer(f"Записей в базе нет.", alert=True)
    else:
        await message.answer(f"Вы уверены что хотите удалить последнюю запись из базы?", reply_markup=yes_no_keyboard())
