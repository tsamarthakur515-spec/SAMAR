

import asyncio
import aiohttp
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio

# ------------------- CONFIG -------------------
API_ID = 33603336
API_HASH = "c9683a8ec3b886c18219f650fc8ed429"
SESSION = "BQIAvwgAtGpTYJxvUNp8rbi2VNdfNGw-foSWWvDtrWSVnLbKeor1FcHdS2DO3WAwKRUHYT9NyJGuBAIjd9cYSh0JGW7SZjxsMTs0xEWFeU7dxKhHatLzbjhIA8kUOxWj2chH_ags_7fIToe7_LFolcHFbdJhCKAuStVEV4bUXvn43vmALgKi87JQHAId5p9xB7atUNHxMebmAOq6JqABdoBCdtUJC7tEov8GBF0a1C4r8WE8wKoSp5vDjcu7mRIJrUcQ17LMHYY6ACErur_iH3zN2Ny7Nd3VYyIu7Fk7VfeErEZlw-EoNvB89m_e_KYWE3E6ITu-vAtHeTAMG_cDo771-c7GAwAAAAIAgPwVAA"
  # replace with your session
# ----------------------------------------------

app = Client("vcbot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)
call = PyTgCalls(app)

# ----------------- COMMANDS ------------------

@app.on_message(filters.command("play", "."))
async def play(client, message):
    if len(message.command) < 2:
        return await message.reply("ᴋᴏɪ sᴏɴɢ ᴋᴀ ɴᴀᴍᴇ ʙᴀᴛᴀᴏ ɴᴀ ʙᴀʙᴜ 🤭\nExample: `.play mann mera `")

    query = message.text.split(None, 1)[1]
    await message.reply(" sᴏɴɢ ᴘʟᴀʏ ʜᴏ ʀᴀʜᴀ ʜᴀɪ ᴛʜᴏᴅᴀ ᴡᴀɪᴛ ᴋɪᴊɪʏᴇ ɴᴀ ʙᴀʙᴜ 💋")

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
        return await message.reply("ʏᴀ ᴡᴀʟᴀ sᴏɴɢ ᴍᴜᴊʜᴇ ɴᴀʜɪ ᴍɪʟᴀ ʀᴀʜᴀ ʜᴀɪ 🥺")

    song = results[0]

    stream_url = song["download"].get("320kbps") or song["download"].get("160kbps")
    title = song.get("title", "Unknown")
    artist = song.get("artist", "Unknown")
    duration = song.get("duration", "Unknown")

    if not stream_url:
        return await message.reply("❌ No playable link found!")

    # Join or change VC stream
    try:
        await call.join_group_call(
            message.chat.id,
            AudioPiped(stream_url, HighQualityAudio())
        )
    except Exception:
        try:
            await call.change_stream(
                message.chat.id,
                AudioPiped(stream_url, HighQualityAudio())
            )
        except Exception as e2:
            return await message.reply(f"⚠️ Could not play in VC: {e2}")

    await message.reply(
        f"🎧 Started Streaming\n\n"
        f"🎵 Title: {title}\n"
        f"👤 Artist: {artist}\n"
        f"⏱  Duration: {duration}\n\n"
        f"🙋 Requested by: {message.from_user.first_name}\n"
        f"🔗 API by: <a href='https://t.me/sxyaru'>Aru x API Bots</a>",
        parse_mode="html"
    )


@app.on_message(filters.command("stop", "."))
async def stop(client, message):
    try:
        await call.leave_group_call(message.chat.id)
        await message.reply("sᴏɴɢ ʙᴀɴᴅ ʜᴏ ɢʏᴀ ʜᴀɪ ʙᴀʙᴜ 🥲")
    except Exception as e:
        await message.reply(f"⚠️ Could not leave VC: {e}")


# ----------------- RUN BOT -------------------
app.start()
call.start()
print("🎵 VC Music Bot Started")
asyncio.get_event_loop().run_forever()
