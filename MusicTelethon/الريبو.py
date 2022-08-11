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


@Client.on_message(    filters.user(SUDO_USERS) & filters.command(["restart"], prefixes=f"{HNDLR}"))
async def restart(client, m: Message):
    await m.delete()
    loli = await m.reply("１")
    await loli.edit("２")
    await loli.edit("３")
    await loli.edit("４")
    await loli.edit("５")
    await loli.edit("６")
    await loli.edit("７")
    await loli.edit("８")
    await loli.edit("９")
    await loli.edit("１０")
    await loli.edit("𝖙𝖎𝖒𝖊 𝖙𝖔 𝖉𝖎𝖊")
    await loli.edit("**🔥 ℜ𝔢𝔟𝔬𝔬𝔱𝔢𝔡 **")
    os.execl(sys.executable, sys.executable, *sys.argv)
    quit()
@Client.on_message(filters.command(["command"], prefixes=f"{HNDLR}"))
async def help(client, m: Message):
    await m.delete()
    HELP = f"""
<b> 𝔅ℜ𝔘ℌ.. {m.from_user.mention}!
- 𝟫𝟫𝟫 ∞ - 𝔗𝔥𝔢 𝔰𝔦𝔱𝔲𝔞𝔱𝔦𝔬𝔫 𝔦𝔰 𝔳𝔢𝔯𝔶 𝔰𝔱𝔯𝔞𝔫𝔤𝔢 ..
ᴢᴏxᴏʟᴏᴠᴇʏᴏ 🌚🔥
——————×—————

🕷 -| ꜰᴏʀ ᴘʟᴀʏ ꜱᴏᴜɴᴅ ɪɴ ᴛʜᴇ ᴄᴀʟʟ   [ `{HNDLR}turn_on + ɴᴀᴍᴇ ᴏꜰ ᴍᴜꜱɪᴄ` ]
🕷 -| ꜰᴏʀ ᴘʟᴀʏ ᴠɪᴅᴇᴏ ɪɴ ᴛʜᴇ ᴄᴀʟʟ   [ `{HNDLR}play_video + ɴᴀᴍᴇ ᴏꜰ ᴠɪᴅᴇᴏ` ]
———————×———————

🕷 -| ᴘᴀᴜꜱᴇ ᴛʜᴇ ꜱᴏɴɢ ᴏʀ ᴠɪᴅᴇᴏ   [ `{HNDLR}resume` ] 
🕷 -| ᴛᴏ ʀᴇᴘʟᴀʏ ᴛʜᴇ ꜱᴏɴɢ  [ `{HNDLR}stop_resume` ]
🕷 -| ᴛᴏ ꜱᴛᴏᴘ ꜱᴏᴜɴᴅ [ `{HNDLR}stop , ending` ] 
———————×———————

🕷 -| ꜰᴏʀ ᴅᴏᴡɴʟᴏᴀᴅ ꜱᴏᴜɴᴅ  [ `{HNDLR}download , install + ɴᴀᴍᴇ ᴏꜰ ᴍᴜꜱɪᴄ ᴏʀ ʟɪɴᴋ` ]
🕷 -| ꜰᴏʀ ᴅᴏᴡɴʟᴏᴀᴅ ᴠɪᴅᴇᴏ  [ `{HNDLR}download_video , install_video + ɴᴀᴍᴇ ᴏꜰ ᴠɪᴅᴇᴏ ᴏʀ ʟɪɴᴋ` ]
———————×———————
🕷 - Z O X O :)
    await m.reply(HELP)
@Client.on_message(filters.command(["repo"], prefixes=f"{HNDLR}"))
async def repo(client, m: Message):
    await m.delete()
    REPO = f"""
<b>𝔥𝔢𝔶 .!{m.from_user.mention}!
-; 𝔅𝔢 𝔴𝔥𝔬 𝔶𝔬𝔲 𝔞𝔯𝔢, 𝔞𝔫𝔡 𝔡𝔬𝔫'𝔱 𝔟𝔢 𝔴𝔥𝔬 𝔱𝔥𝔢 𝔦𝔡𝔦𝔬𝔱𝔰 𝔴𝔞𝔫𝔱 ..
"""
    await m.reply(REPO, disable_web_page_preview=True)
