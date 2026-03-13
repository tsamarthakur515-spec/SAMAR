

import asyncio
import aiohttp
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio

# ------------------- CONFIG -------------------
API_ID = 20898349
API_HASH = "9fdb830d1e435b785f536247f49e7d87"
SESSION = "BQE-4i0ASxu8TXk4s870tFMn-D2Ijs-7DaTep8qcmRnZuowGYTiKDzzy9fKRT3pCc7aFI9oql0Rp5k1FkymDhRbewYPN11p5G7exMCs-z2bdMPuRoJCF60r7p_xq0TBjtLw5P1f-pXHHRxeXSAq0nKyNglv2pZ-GVCbYL4J-OwIkfck4wZyfiU0H58LZla5Il4VmVww-ewK3roa4mVjIxGKYoFva7LqYEf9Iti77jLz7HW7gCfuNessLDXqH1se4DuOSmoJzbacJxofENDQJChGjP4K7gbkMQQKwjCQfndvTmHLyDnc5jDqwfngZK1ogepmyiXZhhzHVebIieznK4DXTM1Q7pAAAAAHKarFXAA"
  # replace with your session
# ----------------------------------------------

app = Client("vcbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
call = PyTgCalls(app)

# ----------------- COMMANDS ------------------

@app.on_message(filters.command("play", "."))
async def play(client, message):
    if len(message.command) < 2:
        return await message.reply("❌ Please provide a song name.\nExample: `.play Sabrina Carpenter`")

    query = message.text.split(None, 1)[1]
    await message.reply("🔎 Searching Saavn...")

    # Fetch song from Flip-Saavn API
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://flip-saavn.vercel.app/search?query={query}"
            async with session.get(url) as resp:
                data = await resp.json()
    except Exception as e:
        return await message.reply(f"⚠️ Failed to fetch API: {e}")

    results = data.get("results")
    if not results:
        return await message.reply("❌ No results found!")

    song = results[0]
    stream_url = song["download"].get("320kbps") or song["download"].get("160kbps")
    title = song.get("title")
    artist = song.get("artist")

    if not stream_url:
        return await message.reply("❌ No playable link found!")

    # Join or change VC stream
    try:
        await call.join_group_call(
            message.chat.id,
            AudioPiped(stream_url, HighQualityAudio())
        )
    except Exception as e:
        try:
            await call.change_stream(
                message.chat.id,
                AudioPiped(stream_url, HighQualityAudio())
            )
        except Exception as e2:
            return await message.reply(f"⚠️ Could not play in VC: {e2}")

    await message.reply(f"▶️ Playing: {title} — {artist}")


@app.on_message(filters.command("stop", "."))
async def stop(client, message):
    try:
        await call.leave_group_call(message.chat.id)
        await message.reply("⏹ Stopped")
    except Exception as e:
        await message.reply(f"⚠️ Could not leave VC: {e}")


# ----------------- RUN BOT -------------------
app.start()
call.start()
print("🎵 VC Music Bot Started")
asyncio.get_event_loop().run_forever()
