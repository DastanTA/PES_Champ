from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllGroupChats, BotCommandScopeAllPrivateChats


async def set_commands(bot: Bot):
    group_commands = [
        BotCommand(
            command='start', description='Начало процесса записи чемпиона.'
        ),
        BotCommand(
            command='help', description='Сюда надо написать текст'
        ),
        BotCommand(
            command='history', description='выгрузка в эксель всех записей'
        ),
        BotCommand(
            command='all_stats', description='показывает кто сколько раз становился чемпионом'
        ),
        BotCommand(
            command='this_year_stats', description='показывает кто сколько раз становился чемпионом'
        ),
        BotCommand(
            command='add_player', description='добавить нового игрока'
        ),
        BotCommand(
            command='cancel', description='останавливает процесс записи итогов чемпионата'
        )
    ]

    private_commands = [
        BotCommand(
            command='start', description='Начало.'
        ),
        BotCommand(
            command='help', description='Сюда надо написать текст'
        )
    ]

    await bot.set_my_commands(group_commands, scope=BotCommandScopeAllGroupChats())
    await bot.set_my_commands(private_commands, scope=BotCommandScopeAllPrivateChats())
