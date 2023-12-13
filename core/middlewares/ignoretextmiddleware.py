from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram import F

from typing import Dict, Any, Callable, Awaitable


class IgnoreTextMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        pass

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if not F.text:
            return await handler(event, data)
        pass
