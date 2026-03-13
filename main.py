import os
import asyncio
import yt_dlp
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped

API_ID = 20898349
API_HASH = "9fdb830d1e435b785f536247f49e7d87"
SESSION = "BQE-4i0ASxu8TXk4s870tFMn-D2Ijs-7DaTep8qcmRnZuowGYTiKDzzy9fKRT3pCc7aFI9oql0Rp5k1FkymDhRbewYPN11p5G7exMCs-z2bdMPuRoJCF60r7p_xq0TBjtLw5P1f-pXHHRxeXSAq0nKyNglv2pZ-GVCbYL4J-OwIkfck4wZyfiU0H58LZla5Il4VmVww-ewK3roa4mVjIxGKYoFva7LqYEf9Iti77jLz7HW7gCfuNessLDXqH1se4DuOSmoJzbacJxofENDQJChGjP4K7gbkMQQKwjCQfndvTmHLyDnc5jDqwfngZK1ogepmyiXZhhzHVebIieznK4DXTM1Q7pAAAAAHKarFXAA"

CHANNEL = "@BAKCHDOI63"

app = Client(
    "vcbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION
)

call = PyTgCalls(app)

songs = {}

os.makedirs("downloads", exist_ok=True)


def download_song(query):
    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "quiet": True,
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)["entries"][0]
        return ydl.prepare_filename(info)


@app.on_message(filters.command("play", "."))
async def play(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ Give song name")

    query = message.text.split(None, 1)[1].lower()

    await message.reply("🔎 Searching in channel...")

    # Search in your Telegram channel
    async for msg in app.search_messages("@BAKCHDOI63", query, filter="audio", limit=1):
        file_id = msg.audio.file_id
        file = await app.download_media(file_id)

        try:
            await call.join_group_call(message.chat.id, AudioPiped(file))
        except:
            await call.change_stream(message.chat.id, AudioPiped(file))

        return await message.reply(f"▶️ Playing: {msg.audio.title}")

    # If song not found
    await message.reply("❌ Song not found in channel!")

@app.on_message(filters.command("stop", "."))
async def stop(client, message):

    await call.leave_group_call(message.chat.id)
    await message.reply("⏹ Stopped")


app.start()
call.start()
print("🎵 VC Music Bot Started")
asyncio.get_event_loop().run_forever()
