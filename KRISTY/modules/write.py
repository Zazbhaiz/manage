from pyrogram import filters
from KRISTY import pbot

@pbot.on_message(filters.command("write"))
async def write(_, message):
    if len(message.command) < 2 :
            return await message.reply_text("`ᴘʟᴇᴀꜱᴇ ɢɪᴠᴇ ᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴡʀɪᴛᴇ ꜰɪʀꜱᴛ ʙᴀʙʏ🖤`")
    m = await message.reply_text("`ᴡʀɪᴛɪɴɢ...`")
    name = message.text.split(None, 1)[1] if len(message.command) < 3 else message.text.split(None, 1)[1].replace(" ", "%20")
    hand = "https://apis.xditya.me/write?text=" + name
    await m.edit("`ᴜᴘʟᴏᴀᴅɪɴɢ ʙᴀʙʏ🖤...`")
    await m.delete()
    await message.reply_photo(hand, caption = "**ᴍᴀᴅᴇ ʙʏ [Kristy](https://t.me/Miss_Kristy_bot)**")


__help__ = """
❍ `/write` <text> : ᴡʀɪᴛᴇꜱ ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ.
"""

__mod_name__ = "Write"
