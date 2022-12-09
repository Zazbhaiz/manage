from platform import python_version as y
from telegram import __version__ as o
from pyrogram import __version__ as z
from telethon import __version__ as s
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import filters
from KRISTY import pbot
from KRISTY.utils.errors import capture_err
from KRISTY.utils.functions import make_carbon


@pbot.on_message(filters.command("carbon"))
@capture_err
async def carbon_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text("`ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴍᴀᴋᴇ ᴄᴀʀʙᴏɴ ʙᴀʙʏ🖤.`")
    if not message.reply_to_message.text:
        return await message.reply_text("`ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴍᴀᴋᴇ ᴄᴀʀʙᴏɴ ʙᴀʙʏ🖤.`")
    m = await message.reply_text("`ᴘʀᴇᴘᴀʀɪɴɢ ᴄᴀʀʙᴏɴ ʙᴀʙʏ🖤`")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("`ᴜᴘʟᴏᴀᴅɪɴɢ ʙᴀʙʏ🖤`")
    await pbot.send_photo(message.chat.id, carbon)
    await m.delete()
    carbon.close()


__mod_name__ = "CARBON"

__help__ = """
ᴍᴀᴋᴇs ᴀ ᴄᴀʀʙᴏɴ ᴏғ ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ ᴀɴᴅ sᴇɴᴅ ɪᴛ ᴛᴏ ʏᴏᴜ.

❍ /carbon *:* ᴍᴀᴋᴇs ᴄᴀʀʙᴏɴ ɪғ ʀᴇᴩʟɪᴇᴅ ᴛᴏ ᴀ ᴛᴇxᴛ

 """
