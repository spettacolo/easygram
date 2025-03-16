from re import split
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.raw.base import message
from pyrogram.types import Message
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram import idle

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
        self.prefixes = ["!", "."]
    
    async def message_manager(self, client, message: Message):
        """Manage incoming messages"""
        # Split only the first word (command) and keep the rest as a single string
        parts = message.text.split(" ", 1)
        command = parts[0]
        args = parts[1] if len(parts) > 1 else None

        if any(command.startswith(prefix) and command[len(prefix):] == "info" for prefix in self.prefixes):
            info = f"Name: {self.client.me.first_name}\nID: {self.client.me.id}\nUsername: {self.client.me.username if self.client.me.username else 'None'}\n"
            await self.edit_message(message.chat.id, message, info)
        else:
            await self.new_message(client, message)
    
    async def edit_message(self, chat_id: int, message: Message, text: str):
        """Edit a message in a chat"""
        await message.edit(text)
        #await self.client.send_message(chat_id, text)

    async def new_message(self, client, message: Message):
        """Reply to a message"""
        print(f"New Message from {message.from_user.first_name} [{message.from_user.id}]\n")

    async def set_handlers(self):
        """Set the handlers for the Easygram client"""
        self.client.add_handler(MessageHandler(self.message_manager, filters.me & filters.command(["info"], prefixes=self.prefixes)))
        self.client.add_handler(MessageHandler(self.new_message))

    async def start(self):
        """Start the Easygram client"""
        await self.client.start()

    async def idle(self):
        """Idle the Easygram client"""
        # Use asyncio.Event to keep the program running until interrupted
        import asyncio
        stop_event = asyncio.Event()
        try:
            await stop_event.wait()
        except KeyboardInterrupt:
            pass

    async def stop(self):
        """Stop the Easygram client"""
        await self.client.stop()