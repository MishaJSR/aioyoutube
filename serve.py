import asyncio

import grpc
import validators
from aiogram import Bot

from grpc_utils.proto import message_pb2, message_pb2_grpc

async def start_progress_bar(bot, tg_user_id, duration_in_seconds, mess_id):
    duration = duration_in_seconds / 200
    num_values = 10
    interval = duration / num_values
    for i in range(num_values):
        await asyncio.sleep(interval)
        progress = round((i + 1) * (100 / num_values))
        await bot.edit_message_text(
            text=f"Статус отправки: {progress}%",
            chat_id=tg_user_id,
            message_id=mess_id,
        )



class MessagingServiceServicer(message_pb2_grpc.MessageServiceServicer):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.last_message_id = None

    def is_valid_url(self, url):
        return validators.url(url)

    async def SendMessage(self, request, context):
        text = request.text
        tg_user_id = request.tg_user_id
        type_mess = request.type_mess
        print(text, tg_user_id, type_mess)
        response = message_pb2.Message(text="Message received: " + request.text)
        if type_mess == "url":
            if self.is_valid_url(text):
                mess = await self.bot.send_message(chat_id=tg_user_id, text="Начало загрузки")
                self.last_message_id = mess.message_id
            else:
                await self.bot.send_message(chat_id=tg_user_id, text="URL неопределен")
        if type_mess == "error_load":
            await self.bot.send_message(chat_id=tg_user_id, text="Ошибка загрузки")
        if type_mess == "error_server":
            await self.bot.send_message(chat_id=tg_user_id, text="Ошибка на стороне сервиса")
        if type_mess == "send_video":
            m = await self.bot.send_message(chat_id=tg_user_id, text="Отправляю видео")
            asyncio.create_task(start_progress_bar(bot=self.bot, tg_user_id=tg_user_id, duration_in_seconds=int(text),
                                                   mess_id = m.message_id))
            self.last_message_id = None
        if type_mess == "progress":
            await self.bot.edit_message_text(
                text=f"Статус загрузки: {text}%",
                chat_id=request.tg_user_id,
                message_id=self.last_message_id,
            )
        return response



async def serve(bot):
    server = grpc.aio.server()
    message_pb2_grpc.add_MessageServiceServicer_to_server(MessagingServiceServicer(bot), server)
    server.add_insecure_port('[::]:50051')
    print("Server starting...")
    await server.start()
    await server.wait_for_termination()
