import asyncio
from os.path import split

from aiogram import types, Router, F
from aiogram.filters import CommandStart

from base_settings import base_settings

admin_main_router = Router()
user_bot_id = base_settings.get_user_bot_id()
static_reg = "regxstate"
static_status = "progress"

@admin_main_router.message(CommandStart())
async def user_start(message: types.Message):
    await message.answer("Чтобы бот вам отправил видео с ютуб, отправьте ему ссылку")

#
# @admin_main_router.message(F.text == "Привет")
# async def user_start(message: types.Message):
#     mess = await message.answer("Чтобы бот вам отправил видео с ютуб, отправьте ему ссылку")
#     await asyncio.sleep(0.1)
#     await message.bot.edit_message_text(
#         text=f"sdasdasdad",
#         chat_id=message.chat.id,
#         message_id=mess.message_id,
#     )

@admin_main_router.message(F.video)
async def user_start(message: types.Message):
    print("get_video")
    try:
        if message.video:
            mes, user_id = message.caption.split(static_reg)
            await message.bot.send_video(chat_id=user_id, video=message.video.file_id)
    except:
        await message.answer(text="Ошибка, отправьте URL")

@admin_main_router.message()
async def user_start(message: types.Message):
    if message.chat.id != user_bot_id:
        await message.bot.send_message(chat_id=user_bot_id, text=message.text+"`"+str(message.chat.id))
#     else:
#         if message.video:
#             mes, user_id = message.caption.split(static_reg)
#             await message.bot.send_video(chat_id=user_id, video=message.video.file_id)
#         else:
#             mes, user_id = message.text.split(static_reg)
#             await message.bot.send_message(chat_id=user_id, text=mes)

