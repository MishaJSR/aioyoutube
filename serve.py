import asyncio

import grpc
from concurrent import futures

from grpc_utils import message_pb2, message_pb2_grpc

class MessagingServiceServicer(message_pb2_grpc.MessageServiceServicer):
    def __init__(self, bot):
        self.bot = bot

    async def SendMessage(self, request, context):
        print(f"Received progress: {request.text}")
        print(f"For chat: {request.tg_user_id}")
        response = message_pb2.Message(text="Message received: " + request.text)
        await self.bot.send_message(chat_id=request.tg_user_id, text=request.text)
        return response



async def serve(bot):
    server = grpc.aio.server()
    message_pb2_grpc.add_MessageServiceServicer_to_server(MessagingServiceServicer(bot), server)
    server.add_insecure_port('[::]:50051')
    print("Server starting...")
    await server.start()
    await server.wait_for_termination()
