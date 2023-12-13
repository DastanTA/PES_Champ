import json

from aiogram import Bot
from aiogram.types import Message


async def get_start(message: Message):
    await message.answer(f"Hi, {message.from_user.first_name}!")

