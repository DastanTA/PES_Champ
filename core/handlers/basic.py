import json

from aiogram import Bot
from aiogram.types import Message


async def get_start(message: Message):
    await message.answer(f"Hi, {message.from_user.first_name}!")


async def get_photo(message: Message, bot: Bot):
    await message.answer("Я сохраню это фото.")
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, f'files/photos/{message.photo[-1].file_id}.jpg')


async def get_hello(message: Message, bot: Bot):
    await message.answer("И тебе привет!")
    json_str = message.model_dump_json(exclude_none=False, indent=4)
    print(json_str)
