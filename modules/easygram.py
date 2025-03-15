from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message
from pyrogram.handlers.message_handler import MessageHandler

class Easygram():
    def __init__(self, api_id: int, api_hash: str, proxy: dict, workdir: str):
        self.api_id = api_id
        self.api_hash = api_hash
        self.proxy = proxy
        self.workdir = workdir
        self.client = Client(
            "easygram",
            api_id=self.api_id,
            api_hash=self.api_hash,
            device_model="Easygram",
            system_version="1.0.0",
            app_version="1.0.0",
            proxy=self.proxy,
            workdir=self.workdir
        )
    
    async def reply_to_message(self, message: Message):
        """Reply to a message"""
        await message.reply("Hello, world!")

    async def set_handlers(self, handlers: list):
        """Set the handlers for the Easygram client"""
        for handler in handlers:
            self.client.add_handler(MessageHandler(self.reply_to_message, filters.all))

    async def start(self):
        """Start the Easygram client"""
        await self.client.start()

    async def stop(self):
        """Stop the Easygram client"""
        await self.client.stop()