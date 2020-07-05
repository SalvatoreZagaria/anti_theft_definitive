import os

from telethon import TelegramClient

api_id = os.environ.get("ANTI_THEFT_API_ID", None)
api_hash = os.environ.get("ANTI_THEFT_API_HASH", None)
session = "anti_theft"

if api_id is None or api_hash is None:
    raise Exception(
        "ANTI_THEFT_API_ID or ANTI_THEFT_API_HASH environment variable missing."
    )

client = TelegramClient(session, api_id, api_hash)


async def send_picture(file_name):
    async with client:
        await client.send_file("me", file_name)


async def send_message(message):
    async with client:
        await client.send_message("me", message)
