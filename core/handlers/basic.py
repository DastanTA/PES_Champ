from datetime import datetime

from aiogram.types import Message

from core.utils.dbconnect import Request
from core.keyboards.inline import first_reg_keyboard, add_player_keyboard, all_players_keyboard, yes_no_keyboard, start_keyboard


votes = dict()

private_instructions = ("Данный бот принимает информацию о том кто стал чемпионом и просто записывает в базу. "
                        "Бот просто помогает отслеживать кто сколько раз становился чемпионом. Можно вывести "
                        "статистику за год или за общее время.\n"
                        "\nПосле того как добавите бота в группу и вызовите команду /start <b>в первый раз</b>, "
                        "вам надо будет зарегистрировать всех игроков, которые будут участовать в чемпионатах. "
                        "При последующих вызовах команды /start будет выводится уже другие компоненты. "
                        "Воспользуйтесь командой /help внутри группы. Там уже будет более детальняя инструкция")

group_instructions = ("Данный бот принимает информацию о том, кто стал чемпионом и просто записывает в базу. "
                      "При самом первом запуске команды /start, бот записывает id группы в базу и единоразово "
                      "дает возможность зарегистрировать всех участников чемпионатов. В последующем можно будет "
                      "добавить нового участника посредством вызова команды /add_player. "
                      "\n\n\n<b>ЧТО ДЕЛАЮТ КОМАНДЫ:</b>"
                      "\n\n<b>/start</b> : "
                      "\n - Если бота добавили в группу в первый раз и это первый вызов, то данная "
                      "команда выведет кнопки 'Добавить меня' и 'готово'. Если нажать на кнопку 'Добавить меня',"
                      "бот зарегистрирует вас в базе. Каждый игрок сам должен на кнопку для регистрации. Кнопка 'готово'"
                      "завершит процесс регистрации и при последующем вызове команды /start в этой группе, будет "
                      "выводится уже другой компонент. Если забыли кого-то зарегать, просто вызовите команду /add_player."
                      "\n - Если не в первый раз: Выводится текст: 'выберите команду' с кнопками под сообщением. Эти "
                      "кнопки и есть команды. Кнопки - просто аналоги тех команд, которые доступны через отправку сообщений"
                      "через вставку '/' в начале."
                      "\n\n<b>/all_stats</b> : "
                      "\nВыводит количество чемпионств каждого игрока за всю историю. Если у игрока вообще нет чемпионств,"
                      "его в списке не будет."
                      "\n\n<b>/all_stats_in_cups</b> : "
                      "\nВыводит количество чемпионств каждого игрока за всю историю. Но вместо количества в виде числа, "
                      "бот покажет то количество кубков рядом с именем, сколько раз он становился чемпионом."
                      " Если у игрока вообще нет чемпионств,"
                      "его в списке не будет."
                      "\n\n<b>/this_year_stats</b> : "
                      "\nВыводит количество чемпионств каждого игрока за текущий год. Если у игрока вообще нет чемпионств,"
                      "его в списке не будет."
                      "\n\n<b>/add_player</b> : "
                      "\nДобавляет нового игрока в базу."
                      "Выводит сообщение с кнопкой. На кнопку должен нажать только тот игрок, который еще не зарегистрирован."
                      "\n\n<b>/all_players</b> : "
                      "\nВыводит список зарегистрированных игроков."
                      "\n\n<b>/cancel</b> : "
                      "\nУдаляет самую последнюю запись чемпиона из базы."
                      "\n\n<b>/help</b> : "
                      "\nПоказывает инструкцию - данное сообщение.")


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
            await message.answer("выберите команду.", reply_markup=start_keyboard())


async def add_result_command(message: Message, request: Request):
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


async def _get_stats_str(request: Request, query_result: dict, answer: str) -> str:
    counter = 1
    for user_id, number in query_result.items():
        player = await request.get_user(user_id)
        answer += f"\n{counter}. {player[0]['first_name']}: <b>{number}</b>"
        counter += 1
    return answer


async def _turn_num_to_cups(number: int) -> str:
    cups = ""
    for i in range(1, number + 1):
        cups += "🏆"
    return cups


async def _get_stats_in_cups(request: Request, query_result: dict, answer: str) -> str:
    counter = 1
    for user_id, number in query_result.items():
        player = await request.get_user(user_id)
        answer += f"\n{counter}. {player[0]['first_name']}: <b>{await _turn_num_to_cups(number)}</b>"
        counter += 1
    return answer


async def show_all_stats(message: Message, request: Request):
    all_stats = await request.get_all_stats(message.chat.id)
    answer = await _get_stats_str(request, all_stats, answer=f"Общая статистика:\n")
    await message.answer(answer)


async def show_all_stats_in_cups(message: Message, request: Request):
    all_stats = await request.get_all_stats(message.chat.id)
    answer = await _get_stats_in_cups(request, all_stats, answer=f"Общая статистика:\n")
    await message.answer(answer)


async def show_this_year_stats(message: Message, request: Request):
    this_year = await request.get_stats_current_year(message.chat.id)
    answer = await _get_stats_str(request, this_year, answer=f"Статистика текущего года:\n")
    await message.answer(answer)


async def cancel_last_record(message: Message, request: Request):
    if not await request.get_any_record(message.chat.id):
        await message.answer(f"Записей в базе нет.", alert=True)
    else:
        await message.answer(f"Вы уверены что хотите удалить последнюю запись из базы?", reply_markup=yes_no_keyboard())


async def show_all_players(message: Message, request: Request):
    all_users = await request.all_users(message.chat.id)
    answer_str = f"Список зарегистрированных игроков:"
    for user in all_users:
        answer_str += f"\n<b>{user['first_name']}</b>"
    await message.answer(answer_str)


async def get_help(message: Message):
    if message.chat.type == 'private':
        await message.answer(f"Салам, {message.from_user.first_name}!"
                             f"\nЧтобы начать пользоваться ботом, надо его сначала в группу добавить."
                             f"\n\n{private_instructions}")

    elif message.chat.type == 'group' or message.chat.type == 'supergroup':
        await message.answer(group_instructions)

