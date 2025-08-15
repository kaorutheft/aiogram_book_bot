import json
import asyncio
import logging
from handlers import other_handlers
from handlers import main_handlers
from config.config import load_config, Config
from services.book_read import read
from keyboards.menu_commands import set_my_commands

from aiogram import Dispatcher, Bot


async def main() -> None:
    # впишите сюда путь папки .env
    config: Config = load_config('сюда в ковычки')
    logger = logging.basicConfig(
        level=config.log.level, format=config.log.format
    )
    bot = Bot(config.bot.token)
    dp = Dispatcher()

    logging.info('Bot is Starting...')
    logging.info('Prepare book...')
    read('и сюда')
    logging.info('Book ready!')

    dp.startup.register(set_my_commands)
    dp.include_router(main_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
