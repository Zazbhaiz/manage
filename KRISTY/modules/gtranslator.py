from gpytranslate import Translator
from telegram.ext import CommandHandler, CallbackContext
from telegram import (
    Message,
    Chat,
    User,
    ParseMode,
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from KRISTY import dispatcher, pbot
from pyrogram import filters
from KRISTY.modules.disable import DisableAbleCommandHandler


__help__ = """ 

ᴜꜱᴇ ᴛʜɪꜱ ᴍᴏᴅᴜʟᴇ ᴛᴏ ᴛʀᴀɴꜱʟᴀᴛᴇ ꜱᴛᴜꜰꜰ!
*ᴄᴏᴍᴍᴀɴᴅꜱ:*
» `/tl` ᴏʀ `/tr`: ᴀꜱ ᴀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ, ᴛʀᴀɴꜱʟᴀᴛᴇꜱ ɪᴛ ᴛᴏ ᴇɴɢʟɪꜱʜ.
» `/tl` <ʟᴀɴɢ>: ᴛʀᴀɴꜱʟᴀᴛᴇꜱ ᴛᴏ <ʟᴀɴɢ>ᴇɢ: /tl ja: ᴛʀᴀɴꜱʟᴀᴛᴇꜱ ᴛᴏ ᴊᴀᴘᴀɴᴇꜱᴇ.
» `/tl` <ꜱᴏᴜʀᴄᴇ>//<ᴅᴇꜱᴛ>: ᴛʀᴀɴꜱʟᴀᴛᴇꜱ ꜰʀᴏᴍ <ꜱᴏᴜʀᴄᴇ> ᴛᴏ <ʟᴀɴɢ>.ᴇɢ:  /ᴛʟ ja//en: ᴛʀᴀɴꜱʟᴀᴛᴇꜱ ꜰʀᴏᴍ ᴊᴀᴘᴀɴᴇꜱᴇ ᴛᴏ ᴇɴɢʟɪꜱʜ.
» `/langs`: ɢᴇᴛ ᴀ ʟɪꜱᴛ ᴏꜰ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ʟᴀɴɢᴜᴀɢᴇꜱ ꜰᴏʀ ᴛʀᴀɴꜱʟᴀᴛɪᴏɴ.

ɪ ᴄᴀɴ ᴄᴏɴᴠᴇʀᴛ ᴛᴇxᴛ ᴛᴏ ᴠᴏɪᴄᴇ ᴀɴᴅ ᴠᴏɪᴄᴇ ᴛᴏ ᴛᴇxᴛ..
» /tts <ʟᴀɴɢ ᴄᴏᴅᴇ>*:* ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ɢᴇᴛ ᴛᴇxᴛ ᴛᴏ ꜱᴘᴇᴇᴄʜ ᴏᴜᴛᴘᴜᴛ
» /stt*:* ᴛʏᴘᴇ ɪɴ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴠᴏɪᴄᴇ ᴍᴇꜱꜱᴀɢᴇ(ꜱᴜᴘᴘᴏʀᴛ ᴇɴɢʟɪꜱʜ ᴏɴʟʏ) ᴛᴏ ᴇxᴛʀᴀᴄᴛ ᴛᴇxᴛ ꜰʀᴏᴍ ɪᴛ.

*Language Codes*
`af,am,ar,az,be,bg,bn,bs,ca,ceb,co,cs,cy,da,de,el,en,eo,es,
et,eu,fa,fi,fr,fy,ga,gd,gl,gu,ha,haw,hi,hmn,hr,ht,hu,hy,
id,ig,is,it,iw,ja,jw,ka,kk,km,kn,ko,ku,ky,la,lb,lo,lt,lv,mg,mi,mk,
ml,mn,mr,ms,mt,my,ne,nl,no,ny,pa,pl,ps,pt,ro,ru,sd,si,sk,sl,
sm,sn,so,sq,sr,st,su,sv,sw,ta,te,tg,th,tl,tr,uk,ur,uz,
vi,xh,yi,yo,zh,zh_CN,zh_TW,zu`
"""

__mod_name__ = "Translator"


trans = Translator()


@pbot.on_message(filters.command(["tl", "tr"]))
async def translate(_, message: Message) -> None:
    reply_msg = message.reply_to_message
    if not reply_msg:
        await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴛʀᴀɴꜱʟᴀᴛᴇ ɪᴛ ʙᴀʙʏ🖤!")
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = await trans.detect(to_translate)
            dest = args
    except IndexError:
        source = await trans.detect(to_translate)
        dest = "en"
    translation = await trans(to_translate, sourcelang=source, targetlang=dest)
    reply = (
        f"<b>Translated from {source} to {dest}</b>:\n"
        f"<code>{translation.text}</code>"
    )

    await message.reply_text(reply, parse_mode="html")


def languages(update: Update, context: CallbackContext) -> None:
    update.effective_message.reply_text(
        "ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ꜱᴇᴇ ᴛʜᴇ ʟɪꜱᴛ ᴏꜰ ꜱᴜᴘᴘᴏʀᴛᴇᴅ ʟᴀɴɢᴜᴀɢᴇ ᴄᴏᴅᴇꜱ ʙᴀʙʏ🖤.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="ʟᴀɴɢᴜᴀɢᴇ ᴄᴏᴅᴇꜱ",
                        url="https://telegra.ph/LANGUAGES-CODE-FOR-KRISTY-BOT-11-07",
                    ),
                ],
            ],
            disable_web_page_preview=True,
        ),
    )


LANG_HANDLER = DisableAbleCommandHandler("langs", languages, run_async=True)

dispatcher.add_handler(LANG_HANDLER)
