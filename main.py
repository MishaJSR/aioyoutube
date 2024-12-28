import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand, Message
import betterlogging as bl

from base_settings import base_settings
from handlers.admin.admin_router import admin_main_router



def get_storage():
    return MemoryStorage()


def setup_logging():
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )


async def on_startup():
    logging.info("Starting bot")


async def on_shutdown(bot):
    logging.info("Shutdown bot")




async def main():
    setup_logging()
    storage = get_storage()
    bot = Bot(token=base_settings.get_token())
    dp = Dispatcher(storage=storage)
    dp.include_routers(admin_main_router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=[BotCommand(command='start', description='Запустить бота')],
                              scope=BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот был выключен!")