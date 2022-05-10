import asyncio
import math
import os
import time
import aiofiles
import aiohttp
import wget
import aiohttp
from io import BytesIO
from traceback import format_exc
from pyrogram import Client, filters
from pyrogram.types import Message
from Python_ARQ import ARQ
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio,    HighQualityVideo,    LowQualityVideo,    MediumQualityVideo
from youtubesearchpython import VideosSearch
from config import HNDLR, bot, call_py
from MusicTelethon.helpers.queues import QUEUE, add_to_queue, get_queue, clear_queue
from MusicTelethon.helpers.decorators import authorized_users_only
from MusicTelethon.helpers.handlers import skip_current_song, skip_item
from pyrogram.errors import FloodWait, MessageNotModified
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL
from MusicTelethon.helpers.merrors import capture_err
ARQ_API_KEY = "QFOTZM-GSZUFY-CHGHRX-TDEHOZ-ARQ"
aiohttpsession = aiohttp.ClientSession()
arq = ARQ("https://thearq.tech", ARQ_API_KEY, aiohttpsession)
def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0
async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(        "yt-dlp",        "-g",        "-f",                "bestaudio",        f"{link}",        stdout=asyncio.subprocess.PIPE,        stderr=asyncio.subprocess.PIPE,    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()
def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        return [songname, url, duration, thumbnail]
    except Exception as e:
        print(e)
        return 0
async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(        "yt-dlp",        "-g",        "-f",              "best[height<=?720][width<=?1280]",        f"{link}",        stdout=asyncio.subprocess.PIPE,        stderr=asyncio.subprocess.PIPE,    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()

@Client.on_message(filters.command(["تشغيل"], prefixes=f"{HNDLR}"))
async def play(client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    m.chat.title
    if replied:
        if replied.audio or replied.voice:
            await m.delete()
            huehue = await replied.reply("** 🕸 𝔭𝔯𝔬𝔠𝔢𝔰𝔰𝔦𝔫𝔤 **")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:35] + "..."
                else:
                    songname = replied.audio.file_name[:35] + "..."
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/d43dcf8e5afbbe66476af.jpg",
                    caption=f"""
**-🕸️𝔱𝔥𝔢 𝔞𝔡𝔡𝔯𝔢𝔰𝔰 -: [{songname}]({link})
-💬 ℑ𝔇 𝔱𝔥𝔢 𝔠𝔥𝔞𝔱 -: {chat_id}
-🕷 𝔯𝔢𝔮𝔲𝔢𝔰𝔱 𝔣𝔯𝔬𝔪 -: {m.from_user.mention}**
""",                )
            else:
                await call_py.join_group_call(                    chat_id,                    AudioPiped(                        dl,                    ),                    stream_type=StreamType().pulse_stream,                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await huehue.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/d43dcf8e5afbbe66476af.jpg",
                    caption=f"""
**-🕸️𝔱𝔥𝔢 𝔞𝔡𝔡𝔯𝔢𝔰𝔰 -: [{songname}]({link})
-💬 ℑ𝔇 𝔱𝔥𝔢 𝔠𝔥𝔞𝔱 -: {chat_id}
-🕷 𝔯𝔢𝔮𝔲𝔢𝔰𝔱 𝔣𝔯𝔬𝔪 -: {m.from_user.mention}**
""",                )

    else:
        if len(m.command) < 2:
            await m.reply("الرد على ملف صوتي أو إعطاء شيء للبحث")
        else:
            await m.delete()
            huehue = await m.reply("🔎 S𝔢𝔞𝔯𝔠𝔥𝔦𝔫𝔤 𝔡𝔢𝔞𝔯 ")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await huehue.edit(" 𝔅ℜ𝔘ℌ!! 𝔫𝔬𝔱𝔥𝔦𝔫𝔤 𝔴𝔞𝔰 𝔣𝔬𝔲𝔫𝔡 ")
            else:
                songname = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"** S𝔬𝔯𝔯𝔶 𝔱𝔥𝔢𝔯𝔢 𝔦𝔰 𝔞𝔫 𝔢𝔯𝔯𝔬𝔯 ** \n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await huehue.delete()
                        await m.reply_photo(
                            photo=f"{thumbnail}",
                            caption=f"""
**-🕸️𝔱𝔥𝔢 𝔞𝔡𝔡𝔯𝔢𝔰𝔰 -: [{songname}]({link})
-⏱️ 𝔳𝔦𝔡𝔢𝔬 𝔡𝔲𝔯𝔞𝔱𝔦𝔬𝔫 -: {duration}
-💬 ℑ𝔇 𝔱𝔥𝔢 𝔠𝔥𝔞𝔱 -: {chat_id}
-🕷 𝔯𝔢𝔮𝔲𝔢𝔰𝔱 𝔣𝔯𝔬𝔪 -: {m.from_user.mention}**
""",
                        )
                    else:
                        try:
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().pulse_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await huehue.delete()
                            # await m.reply_to_message.delete()
                            await m.reply_photo(
                                photo=f"{thumbnail}",
                                caption=f"""
**-🕸️𝔱𝔥𝔢 𝔞𝔡𝔡𝔯𝔢𝔰𝔰 -: [{songname}]({link})
-⏱️ 𝔳𝔦𝔡𝔢𝔬 𝔡𝔲𝔯𝔞𝔱𝔦𝔬𝔫 -: {duration}
-💬 ℑ𝔇 𝔱𝔥𝔢 𝔠𝔥𝔞𝔱 -: {chat_id}
-🕷 𝔯𝔢𝔮𝔲𝔢𝔰𝔱 𝔣𝔯𝔬𝔪 -: {m.from_user.mention}**
""",
                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")


@Client.on_message(filters.command(["تشغيل_فيديو"], prefixes=f"{HNDLR}"))
async def vplay(client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    m.chat.title
    if replied:
        if replied.video or replied.document:
            await m.delete()
            huehue = await replied.reply("**🕸 𝔇𝔬𝔴𝔫𝔩𝔬𝔞𝔡𝔦𝔫𝔤 𝔞𝔫𝔡 𝔭𝔯𝔬𝔠𝔢𝔰𝔰𝔦𝔫𝔤 **")
            dl = await replied.download()
            link = replied.link
            if len(m.command) < 2:
                Q = 720
            else:
                pq = m.text.split(None, 1)[1]
                if pq == "720" or "480" or "360":
                    Q = int(pq)
                else:
                    Q = 720
                    await huehue.edit(                        "𝔒𝔫𝔩𝔶 𝔱𝔥𝔢 𝔣𝔬𝔩𝔩𝔬𝔴𝔦𝔫𝔤 𝔞𝔯𝔢 𝔞𝔩𝔩𝔬𝔴𝔢𝔡:  ７２０ ، ４８０ ، ３６０ \𝔫 - ℑ𝔱'𝔰 𝔠𝔬𝔪𝔦𝔫𝔤 𝔡𝔬𝔴𝔫 𝔯𝔦𝔤𝔥𝔱 𝔫𝔬𝔴   ７２０ 𝔭𝔦𝔵𝔢𝔩   "                 )

            if replied.video:
                songname = replied.video.file_name[:35] + "..."
            elif replied.document:
                songname = replied.document.file_name[:35] + "..."

            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/d43dcf8e5afbbe66476af.jpg",
                    caption=f"""
**-🕸️𝔱𝔥𝔢 𝔞𝔡𝔡𝔯𝔢𝔰𝔰 -: [{songname}]({link})
-💬 ℑ𝔇 𝔱𝔥𝔢 𝔠𝔥𝔞𝔱 -: {chat_id}
-🕷 𝔯𝔢𝔮𝔲𝔢𝔰𝔱 𝔣𝔯𝔬𝔪 -: {m.from_user.mention}**
""",
                )
            else:
                if Q == 720:
                    hmmm = HighQualityVideo()
                elif Q == 480:
                    hmmm = MediumQualityVideo()
                elif Q == 360:
                    hmmm = LowQualityVideo()
                await call_py.join_group_call(
                    chat_id,
                    AudioVideoPiped(dl, HighQualityAudio(), hmmm),
                    stream_type=StreamType().pulse_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Video", Q)
                await huehue.delete()
                # await m.reply_to_message.delete()
                await m.reply_photo(
                    photo="https://telegra.ph/file/d43dcf8e5afbbe66476af.jpg",
                    caption=f"""
**-🕸️𝔱𝔥𝔢 𝔞𝔡𝔡𝔯𝔢𝔰𝔰 -: [{songname}]({link})
-💬 ℑ𝔇 𝔱𝔥𝔢 𝔠𝔥𝔞𝔱 -: {chat_id}
-🕷 𝔯𝔢𝔮𝔲𝔢𝔰𝔱 𝔣𝔯𝔬𝔪 -: {m.from_user.mention}**
""",                )

    else:
        if len(m.command) < 2:
            await m.reply(                "**الرد على ملف صوتي أو إعطاء شيء للبحث**"            )
        else:
            await m.delete()
            huehue = await m.reply("**🔎 S𝔢𝔞𝔯𝔠𝔥𝔦𝔫𝔤 𝔡𝔢𝔞𝔯 ")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            Q = 720
            hmmm = HighQualityVideo()
            if search == 0:
                await huehue.edit(                    "**𝔫𝔬𝔱𝔥𝔦𝔫𝔤 𝔴𝔞𝔰 𝔣𝔬𝔲𝔫𝔡**"                )
            else:
                songname = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                hm, ytlink = await ytdl(url)
                if hm == 0:
                    await huehue.edit(f"**S𝔬𝔯𝔯𝔶 𝔱𝔥𝔢𝔯𝔢 𝔦𝔰 𝔞𝔫 𝔢𝔯𝔯𝔬𝔯  ⚠️** \n\n`{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                        await huehue.delete()
                        await m.reply_photo(
                            photo=f"{thumbnail}",
                            caption=f"""
**-🕸 𝔱𝔥𝔢 𝔞𝔡𝔡𝔯𝔢𝔰𝔰 -: [{songname}]({link})
-⏱ 𝔳𝔦𝔡𝔢𝔬 𝔡𝔲𝔯𝔞𝔱𝔦𝔬𝔫 -: {duration}
-💬 ℑ𝔇 𝔱𝔥𝔢 𝔠𝔥𝔞𝔱 -: {chat_id}
-🕷 𝔯𝔢𝔮𝔲𝔢𝔰𝔱 𝔣𝔯𝔬𝔪 -: {m.from_user.mention}**
""",                        )
                    else:
                        try:
                            await call_py.join_group_call(                                chat_id,                                AudioVideoPiped(ytlink, HighQualityAudio(), hmmm),                                stream_type=StreamType().pulse_stream,                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Video", Q)
                            await huehue.delete()
                            await m.reply_photo(
                                photo=f"{thumbnail}",
                                caption=f"""
**-🕸️𝔱𝔥𝔢 𝔞𝔡𝔡𝔯𝔢𝔰𝔰 -: [{songname}]({link})
-⏱️ 𝔳𝔦𝔡𝔢𝔬 𝔡𝔲𝔯𝔞𝔱𝔦𝔬𝔫 -: {duration}
-💬 ℑ𝔇 𝔱𝔥𝔢 𝔠𝔥𝔞𝔱 -: {chat_id}
-🕷 𝔯𝔢𝔮𝔲𝔢𝔰𝔱 𝔣𝔯𝔬𝔪 -: {m.from_user.mention}**
""",                            )
                        except Exception as ep:
                            await huehue.edit(f"`{ep}`")


@Client.on_message(filters.command(["اغنيه عشوائية"], prefixes=f"{HNDLR}"))
async def playfrom(client, m: Message):
    chat_id = m.chat.id
    if len(m.command) < 2:
        await m.reply(            f"**استخدام :** \n\n`{HNDLR}اغنيه عشوائيه  [قم بوضع جانب الامر معرف المحادثه او ايدي المحادثه]` \n"        )
    else:
        args = m.text.split(maxsplit=1)[1]
        if ";" in args:
            chat = args.split(";")[0]
            limit = int(args.split(";")[1])
        else:
            chat = args
            limit = 10
            lmt = 9
        await m.delete()
        hmm = await m.reply(f"🔎 𝔗𝔞𝔨𝔢𝔰  {limit} 𝔯𝔞𝔫𝔡𝔬𝔪 𝔰𝔬𝔫𝔤 𝔣𝔯𝔬𝔪  {chat}**")
        try:
            async for x in bot.search_messages(chat, limit=limit, filter="audio"):
                location = await x.download()
                if x.audio.title:
                    songname = x.audio.title[:30] + "..."
                else:
                    songname = x.audio.file_name[:30] + "..."
                link = x.link
                if chat_id in QUEUE:
                    add_to_queue(chat_id, songname, location, link, "Audio", 0)
                else:
                    await call_py.join_group_call(                        chat_id,                        AudioPiped(location),                        stream_type=StreamType().pulse_stream,                    )
                    add_to_queue(chat_id, songname, location, link, "Audio", 0)
                    await m.reply_photo(
                        photo="https://telegra.ph/file/d43dcf8e5afbbe66476af.jpg",
                        caption=f"""
**-▶ S𝔱𝔞𝔯𝔱 𝔭𝔩𝔞𝔶𝔦𝔫𝔤 𝔰𝔬𝔫𝔤𝔰 𝔣𝔯𝔬𝔪 - {chat}
-🕸️ 𝔱𝔥𝔢 𝔞𝔡𝔡𝔯𝔢𝔰𝔰 -: [{songname}]({link})
-💬 𝔱𝔥𝔢 𝔠𝔥𝔞𝔱 -: {chat_id}
-🕷 𝔯𝔢𝔮 𝔣𝔯𝔬𝔪 -: {m.from_user.mention}**
""",                    )
            await hmm.delete()
            await m.reply(                f"➕ اضافه {lmt} أغنية في قائمة الانتظار \n• ارسل {HNDLR}التشغيل_التلقائي لاضاف اغنيه في القائمه الانتضار**"            )
        except Exception as e:
            await hmm.edit(f"**𝔗𝔥𝔢𝔯𝔢 𝔢𝔯𝔯𝔬𝔯 ** \n`{e}`")


@Client.on_message(filters.command(["التشغيل التلقائي", "queue"], prefixes=f"{HNDLR}"))
async def playlist(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await m.delete()
            await m.reply(                f"**🎧 𝔯𝔲𝔫𝔫𝔦𝔫𝔤 𝔫𝔬𝔴 :** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}`",                disable_web_page_preview=True,            )
        else:
            QUE = f"**🎧 تشغيل الان :** \n[{chat_queue[0][0]}]({chat_queue[0][2]}) | `{chat_queue[0][3]}` \n\n**⏯ 𝔚𝔞𝔦𝔱𝔦𝔫𝔤 𝔩𝔦𝔰𝔱 :**"
            l = len(chat_queue)
            for x in range(1, l):
                hmm = chat_queue[x][0]
                hmmm = chat_queue[x][2]
                hmmmm = chat_queue[x][3]
                QUE = QUE + "\n" + f"**#{x}** - [{hmm}]({hmmm}) | `{hmmmm}`\n"
            await m.reply(QUE, disable_web_page_preview=True)
    else:
        await m.reply("**❌ 𝔗𝔥𝔢𝔯𝔢 𝔦𝔰 𝔫𝔬 𝔫𝔢𝔵𝔱 𝔯𝔲𝔫 **")
@Client.on_message(filters.command(["التالي"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def skip(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("**❌ 𝔗𝔥𝔢𝔯𝔢 𝔦𝔰 𝔫𝔬𝔱𝔥𝔦𝔫𝔤 𝔦𝔫 𝔱𝔥𝔢 𝔮𝔲𝔢𝔲𝔢 𝔱𝔬 𝔰𝔨𝔦𝔭 !**")
        elif op == 1:
            await m.reply("𝔈𝔪𝔭𝔱𝔶 𝔮𝔲𝔢𝔲𝔢, 𝔩𝔢𝔞𝔳𝔢 𝔳𝔬𝔦𝔠𝔢 𝔠𝔥𝔞𝔱**")
        else:
            await m.reply(                f"**⏭ تخطي التشغيل ** \n**🎧 التشغيل الان** - [{op[0]}]({op[1]}) | `{op[2]}`",                disable_web_page_preview=True,            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "**🗑️ 𝔗𝔥𝔢 𝔣𝔬𝔩𝔩𝔬𝔴𝔦𝔫𝔤 𝔰𝔬𝔫𝔤𝔰 𝔥𝔞𝔳𝔢 𝔟𝔢𝔢𝔫 𝔯𝔢𝔪𝔬𝔳𝔢𝔡 𝔣𝔯𝔬𝔪 𝔱𝔥𝔢 𝔮𝔲𝔢𝔲𝔢 : -**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#⃣{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(filters.command(["انهاء", "ايقاف"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def stop(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("**🩸 ℑ𝔱 𝔥𝔞𝔰 𝔟𝔢𝔢𝔫 𝔰𝔲𝔠𝔠𝔢𝔰𝔰𝔣𝔲𝔩𝔩𝔶 𝔰𝔥𝔲𝔱 𝔡𝔬𝔴𝔫 **")
        except Exception as e:
            await m.reply(f"**𝔗𝔥𝔢𝔯𝔢 𝔢𝔯𝔯𝔬𝔯 ** \n`{e}`")
    else:
        await m.reply("**❌ 𝔗𝔥𝔢𝔯𝔢 𝔦𝔰 𝔫𝔬 𝔴𝔬𝔯𝔨𝔦𝔫𝔤 𝔰𝔬𝔫𝔤  !**")
@Client.on_message(filters.command(["استئناف"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def pause(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(                f"**⏸ تم إيقاف التشغيل مؤقتًا.**\n\n• يمكنك ارجاع التشغيل بواسطه ارسال امر  » `{HNDLR}ايقاف_الاستئناف`"            )
        except Exception as e:
            await m.reply(f"**𝔗𝔥𝔢𝔯𝔢 𝔢𝔯𝔯𝔬𝔯 ** \n`{e}`")
    else:
        await m.reply("** ❌ 𝔗𝔥𝔢𝔯𝔢 𝔦𝔰 𝔫𝔬 𝔭𝔩𝔞𝔶𝔦𝔫𝔤 𝔰𝔬𝔫𝔤 !**") 
@Client.on_message(filters.command(["ايقاف_الاستئناف"], prefixes=f"{HNDLR}"))
@authorized_users_only
async def resume(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(                f"**▶  ℜ𝔢𝔰𝔲𝔪𝔢 𝔭𝔞𝔲𝔰𝔢𝔡 𝔭𝔩𝔞𝔶𝔟𝔞𝔠𝔨  **"            )
        except Exception as e:
            await m.reply(f"**𝔗𝔥𝔢𝔯𝔢 𝔢𝔯𝔯𝔬𝔯 ** \n`{e}`")
    else:
        await m.reply("**❌ 𝔑𝔬𝔱𝔥𝔦𝔫𝔤 𝔦𝔰 𝔠𝔲𝔯𝔯𝔢𝔫𝔱𝔩𝔶 𝔭𝔞𝔲𝔰𝔢𝔡 !**")
