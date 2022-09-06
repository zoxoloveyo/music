import os
import sys
from datetime import datetime
from time import time
from pyrogram import Client, filters
from pyrogram.types import Message
from config import HNDLR, SUDO_USERS
START_TIME = datetime.utcnow()
TIME_DURATION_UNITS = (    ("Minggu", 60 * 60 * 24 * 7),    ("Hari", 60 * 60 * 24),    ("Jam", 60 * 60),    ("Menit", 60),    ("Detik", 1),)
async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else ""))
    return ", ".join(parts)


@Client.on_message(    filters.user(SUDO_USERS) & filters.command(["ريستارت"], prefixes=f"{HNDLR}"))
async def restart(client, m: Message):
    await m.delete()
    loli = await m.reply("1")
    await loli.edit("2")
    await loli.edit("3")
    await loli.edit("4")
    await loli.edit("5")
    await loli.edit("6")
    await loli.edit("7")
    await loli.edit("8")
    await loli.edit("9")
    await loli.edit("**🔥 ℜ𝔢𝔟𝔬𝔬𝔱𝔢𝔡 **")
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()
@Client.on_message(filters.command(["الأوامر"], prefixes=f"{HNDLR}"))
async def help(client, m: Message):
    await m.delete()
    HELP = f"""
<b> 𝔅ℜ𝔘ℌ.. {m.from_user.mention}!
- 𝟫𝟫𝟫 ∞ - 𝔗𝔥𝔢 𝔰𝔦𝔱𝔲𝔞𝔱𝔦𝔬𝔫 𝔦𝔰 𝔳𝔢𝔯𝔶 𝔰𝔱𝔯𝔞𝔫𝔤𝔢 ..
ᴢᴏxᴏʟᴏᴠᴇʏᴏ 🌚🔥
——————×—————

🕷 -| لتشغيل صوتية في المكالمة أرسل ⇦ [ `{HNDLR}تشغيل  + اسم الاغنية` ]
🕷 -| لتشغيل فيديو في المكالمة  ⇦ [ `{HNDLR}تشغيل_فيديو  + اسم الاغنية` ]
———————×———————

🕷 -| لأيقاف الاغنية او الفيديو مؤقتآ  ⇦ [ `{HNDLR}استئناف` ] 
🕷 -| لأعاده تشغيل الاغنية ⇦  [ `{HNDLR}ايقاف_الاستئناف` ]
🕷 -| لأيقاف الاغنية  ⇦ [ `{HNDLR}ايقاف` ] 
———————×———————

🕷 -| لتحميل صوتية أرسل ⇦ [ `{HNDLR}تحميل + اسم الاغنية او الرابط` ]
🕷 -| لتحميل فيديو  ⇦  [ `{HNDLR}تحميل_فيديو + اسم الاغنية او الرابط` ]
———————×———————

🕷 -| لأعاده تشغيل التنصيب أرسل ⇦  [ `{HNDLR}ريستارت` ]
———————×———————
🛠 -| ZoxoLoveyo
⭐ -| @ZOXOANGEL"""
    await m.reply(HELP)
@Client.on_message(filters.command(["الريبو"], prefixes=f"{HNDLR}"))
async def repo(client, m: Message):
    await m.delete()
    REPO = f"""
<b>𝔥𝔢𝔶 .!{m.from_user.mention}!
-; 𝔅𝔢 𝔴𝔥𝔬 𝔶𝔬𝔲 𝔞𝔯𝔢, 𝔞𝔫𝔡 𝔡𝔬𝔫'𝔱 𝔟𝔢 𝔴𝔥𝔬 𝔱𝔥𝔢 𝔦𝔡𝔦𝔬𝔱𝔰 𝔴𝔞𝔫𝔱 ..
⚔️  | @ZOXOANGEL
"""
    await m.reply(REPO, disable_web_page_preview=True)
