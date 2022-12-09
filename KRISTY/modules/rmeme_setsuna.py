import datetime
import codecs
import html
import os
import random
import re
import subprocess
import requests as r
from KRISTY import dispatcher 

from telegram.error import BadRequest
from telegram.ext import CommandHandler, Filters, run_async, MessageHandler 
from telegram.utils.helpers import escape_markdown, mention_html
from telegram import (
    Chat,
    ChatAction,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    MessageEntity,
    ParseMode,
    TelegramError,
)




@run_async
def rmemes(update, context):
    msg = update.effective_message
    chat = update.effective_chat
    context.bot.send_chat_action(chat.id, action="upload_photo")

    SUBREDS = [
        "Animemes"
        "hentaimemes"
        "meirl",
        "dankmemes",
        "AdviceAnimals",
        "memes",
        "meme",
        "memes_of_the_dank",
        "PornhubComments",
        "teenagers",
        "memesIRL",
        "insanepeoplefacebook",
        "terriblefacebookmemes",
    ]

    subreddit = random.choice(SUBREDS)
    res = r.get(f"https://meme-api.herokuapp.com/gimme/{subreddit}")

    if res.status_code != 200:  # Like if api is down?
        msg.reply_text("ꜱᴏʀʀʏ ꜱᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ :(, ᴘᴏꜱꜱɪʙʟʏ ᴀᴘɪ ɪꜱ ᴅᴏᴡɴ ʙᴀʙʏ🖤")
        return
    else:
        res = res.json()

    rpage = res.get(str("subreddit"))  # Subreddit
    title = res.get(str("title"))  # Post title
    memeu = res.get(str("url"))  # meme pic url
    plink = res.get(str("postLink"))

    caps = f"× <b>Title</b>: {title}\n"
    caps += f"× <b>Subreddit:</b> <pre>r/{rpage}</pre>"

    keyb = [[InlineKeyboardButton(text="ᴘᴏꜱᴛʟɪɴᴋ 🔗", url=plink)]]
    try:
        context.bot.send_photo(
            chat.id,
            photo=memeu,
            caption=(caps),
            reply_markup=InlineKeyboardMarkup(keyb),
            timeout=60,
            parse_mode=ParseMode.HTML,
        )

    except BadRequest as excp:
        return msg.reply_text(f"ᴇʀʀᴏʀ! {excp.message} ʙᴀʙʏ🖤")

@run_async
def anyy(update, context):
    msg = update.effective_message
    chat = update.effective_chat
    
    context.bot.send_chat_action(chat.id, action="upload_photo")
    try:
      sub = msg.text.split(" ", 1)[1]
    except IndexError:
      sub = msg.text[3:]
    if sub == " ": 
      return msg.reply_text("ᴡʜᴀᴛ ᴛᴏ ꜱᴄʀᴀᴘᴇ ꜰᴏʀ ʙᴀʙʏ🖤?") 
    print(sub)
    res = r.get(f"https://meme-api.herokuapp.com/gimme/{sub}")
    j = res.json()

    if res.status_code != 200:  # Like if api is down?
        if j.get(str('code')) == str(404):
          return msg.reply_text("ᴀʜʜ ꜰ, ᴛʜɪꜱ ꜱᴜʙ ᴅᴏᴇꜱɴ'ᴛ ᴇxɪꜱᴛ ʙᴀʙʏ🖤!!")
        msg.reply_text("ꜱᴏʀʀʏ ꜱᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ :(, ᴘᴏꜱꜱɪʙʟʏ ᴀᴘɪ ɪꜱ ᴅᴏᴡɴ ʙᴀʙʏ🖤")
        return
    else:
        res = res.json()

    rpage = res.get(str("subreddit"))  # Subreddit
    title = res.get(str("title"))  # Post title
    memeu = res.get(str("url"))  # meme pic url
    plink = res.get(str("postLink"))

    caps = f"× <b>TITLE</b>: {title}\n"
    caps += f"× <b>subreddit:</b> <pre>r/{rpage}</pre>"

    keyb = [[InlineKeyboardButton(text="ᴘᴏꜱᴛʟɪɴᴋ 🔗", url=plink)]]
    try:
        context.bot.send_photo(
            chat.id,
            photo=memeu,
            caption=(caps),
            reply_markup=InlineKeyboardMarkup(keyb),
            timeout=60,
            parse_mode=ParseMode.HTML,
        )

    except BadRequest as excp:
        return msg.reply_text(f"ᴇʀʀᴏʀ! {excp.message} ʙᴀʙʏ🖤")
       

__help__ = """
***Rmeme Module**
`/rmeme`: ᴛʀʏ ɪᴛ ᴜʀꜱᴇʟꜰ
""" 
R_HANDLER = CommandHandler("rmeme", rmemes)
DIS_HANDLER = CommandHandler("r", anyy)
COS_HANDLER = MessageHandler(Filters.regex(r'^/r\/(.*)'), anyy)
dispatcher.add_handler(R_HANDLER)
dispatcher.add_handler(COS_HANDLER)
dispatcher.add_handler(DIS_HANDLER)

__mod_name__ = "Rmeme"
