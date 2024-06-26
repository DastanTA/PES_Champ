from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllGroupChats, BotCommandScopeAllPrivateChats


async def set_commands(bot: Bot):
    group_commands = [
        BotCommand(
            command='start', description='Старт. Рег или команды.'
        ),BotCommand(
            command='add_result', description='Начало процесса записи чемпиона.'
        ),
        BotCommand(
            command='all_stats', description='показывает кто сколько раз становился чемпионом за все время'
        ),
        BotCommand(
            command='all_stats_in_cups', description='показывает кто сколько раз становился чемпионом за все время'
        ),
        BotCommand(
            command='this_year_stats', description='показывает кто сколько раз становился чемпионом в этом году'
        ),
        BotCommand(
            command='add_player', description='добавить нового игрока'
        ),
        BotCommand(
            command='all_players', description='Список зареганных игроков'
        ),
        BotCommand(
            command='cancel', description='удаляет последнюю запись'
        ),
        BotCommand(
            command='help', description='инструкции'
        )
    ]

    private_commands = [
        BotCommand(
            command='start', description='Начало.'
        ),
        BotCommand(
            command='help', description='инструкция'
        )
    ]

    await bot.set_my_commands(group_commands, scope=BotCommandScopeAllGroupChats())
    await bot.set_my_commands(private_commands, scope=BotCommandScopeAllPrivateChats())
