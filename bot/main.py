import asyncio

from aiogram import Bot, types, F
from aiogram.dispatcher.dispatcher import Dispatcher

from config import settings
from handlers import rt

bot = Bot(token=settings.BOT_TOKEN.get_secret_value())

dp = Dispatcher()


async def main() -> None:
    dp.include_router(rt)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
