from datetime import datetime

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from KRISTY import OWNER_ID
from KRISTY import OWNER_USERNAME as uWu
from KRISTY import START_IMG, SUPPORT_CHAT, pbot
from KRISTY.utils.errors import capture_err


def content(msg: Message) -> [None, str]:
    text_to_return = msg.text

    if msg.text is None:
        return None
    if " " in text_to_return:
        try:
            return msg.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


@pbot.on_message(filters.command("bug"))
@capture_err
async def bug(_, msg: Message):
    if msg.chat.username:
        chat_username = f"@{msg.chat.username}/`{msg.chat.id}` ʙᴀʙʏ🖤"
    else:
        chat_username = f"ᴩʀɪᴠᴀᴛᴇ ɢʀᴏᴜᴩ/`{msg.chat.id}` ʙᴀʙʏ🖤"

    bugs = content(msg)
    user_id = msg.from_user.id
    mention = (
        "[" + msg.from_user.first_name + "](tg://user?id=" + str(msg.from_user.id) + ")"
    )
    datetimes_fmt = "%d-%m-%Y"
    datetimes = datetime.utcnow().strftime(datetimes_fmt)

    bug_report = f"""
**#ʙᴜɢ :** @{uWu}

**ʀᴇᴩᴏʀᴛᴇᴅ ʙʏ :** {mention}
**ᴜsᴇʀ ɪᴅ :** {user_id}
**ᴄʜᴀᴛ : {chat_username}

**ʙᴜɢ :** {bugs}

**ᴇᴠᴇɴᴛ sᴛᴀᴍᴩ :** {datetimes}"""

    if msg.chat.type == "private":
        await msg.reply_text("<b>» ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴩs ʙᴀʙʏ🖤.</b>")
        return

    if user_id == OWNER_ID:
        if bugs:
            await msg.reply_text(
                "<b>» ᴀʀᴇ ʏᴏᴜ ᴄᴏᴍᴇᴅʏ ᴍᴇ  ʙᴀʙʏ🖤, ʏᴏᴜ'ʀᴇ ᴛʜᴇ ᴏᴡɴᴇʀ ᴏғ ᴛʜᴇ ʙᴏᴛ.</b>",
            )
            return
        else:
            await msg.reply_text("ʜᴜᴛɪʏᴀ ᴏᴡɴᴇʀ ʙᴀʙʏ🖤!")
    elif user_id != OWNER_ID:
        if bugs:
            await msg.reply_text(
                f"<b>ʙᴜɢ ʀᴇᴩᴏʀᴛ : {bugs}</b>\n\n"
                "<b>» ʙᴜɢ sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇᴩᴏʀᴛᴇᴅ ᴀᴛ sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ ʙᴀʙʏ🖤!</b>",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data=f"close_reply")]]
                ),
            )
            await pbot.send_photo(
                SUPPORT_CHAT,
                photo=START_IMG,
                caption=f"{bug_report}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("• ᴠɪᴇᴡ ʙᴜɢ •", url=f"{msg.link}")],
                        [
                            InlineKeyboardButton(
                                "• ᴄʟᴏsᴇ •", callback_data="close_send_photo"
                            )
                        ],
                    ]
                ),
            )
        else:
            await msg.reply_text(
                f"<b>» ɴᴏ ʙᴜɢ ᴛᴏ ʀᴇᴩᴏʀᴛ ʙᴀʙʏ🖤!</b>",
            )


@pbot.on_callback_query(filters.regex("close_reply"))
async def close_reply(msg, CallbackQuery):
    await CallbackQuery.message.delete()


@pbot.on_callback_query(filters.regex("close_send_photo"))
async def close_send_photo(_, CallbackQuery):
    if CallbackQuery.from_user.id != OWNER_ID:
        return await CallbackQuery.answer(
            "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ʀɪɢʜᴛs ᴛᴏ ᴄʟᴏsᴇ ᴛʜɪs ʙᴀʙʏ🖤.", show_alert=True
        )
    else:
        await CallbackQuery.message.delete()


__help__ = """
*ғᴏʀ ʀᴇᴩᴏʀᴛɪɴɢ ᴀ ʙᴜɢ ɪɴ ᴋʀɪꜱᴛʏ
 ❍ /bug *:* ᴛᴏ ʀᴇᴩᴏʀᴛ ᴀ ʙᴜɢ ᴀᴛ sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ.
"""
__mod_name__ = "BUG"
