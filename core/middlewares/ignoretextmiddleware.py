from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery, Message, BotCommand

from typing import Dict, Any, Callable, Awaitable


class IgnoreOthersMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, (CallbackQuery, Message, BotCommand)):
            print("Catched")
            return await handler(event, data)
        print(f"Didn't catch\n{event}")
        return
