import os
import re
import math
import requests
import cloudscraper
import urllib.request as urllib
from PIL import Image
from html import escape
from bs4 import BeautifulSoup as bs

from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram import TelegramError, Update
from telegram.ext import CallbackContext
from telegram.utils.helpers import mention_html

from KRISTY import dispatcher
from KRISTY.modules.disable import DisableAbleCommandHandler

combot_stickers_url = "https://combot.org/telegram/stickers?q="


def stickerid(update: Update, context: CallbackContext):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
        update.effective_message.reply_text(
            "ʜᴇʏ ʙᴀʙʏ🖤"
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", ᴛʜᴇ ꜱᴛɪᴄᴋᴇʀ ɪᴅ ʏᴏᴜ ᴀʀᴇ ʀᴇᴘʟʏɪɴɢ ɪꜱ :\n <code>"
            + escape(msg.reply_to_message.sticker.file_id)
            + "</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text(
            "ʜᴇʏ ʙᴀʙʏ🖤 "
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", ᴘʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴛᴏ ꜱᴛɪᴄᴋᴇʀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ɢᴇᴛ ɪᴅ ꜱᴛɪᴄᴋᴇʀ",
            parse_mode=ParseMode.HTML,
        )


def kang(update, context):
    msg = update.effective_message
    user = update.effective_user
    args = context.args
    packnum = 0
    packname = "a" + str(user.id) + "_by_" + context.bot.username
    packname_found = 0
    max_stickers = 120

    while packname_found == 0:
        try:
            stickerset = context.bot.get_sticker_set(packname)
            if len(stickerset.stickers) >= max_stickers:
                packnum += 1
                packname = (
                    "a"
                    + str(packnum)
                    + "_"
                    + str(user.id)
                    + "_by_"
                    + context.bot.username
                )
            else:
                packname_found = 1
        except TelegramError as e:
            if e.message == "Stickerset_invalid":
                packname_found = 1
    kangsticker = "kangsticker.png"
    is_animated = False
    file_id = ""

    if msg.reply_to_message:
        if msg.reply_to_message.sticker:
            if msg.reply_to_message.sticker.is_animated:
                is_animated = True
            file_id = msg.reply_to_message.sticker.file_id

        elif msg.reply_to_message.photo:
            file_id = msg.reply_to_message.photo[-1].file_id
        elif msg.reply_to_message.document:
            file_id = msg.reply_to_message.document.file_id
        else:
            msg.reply_text("ʏᴇᴀ, ɪ ᴄᴀɴ'ᴛ ᴋᴀɴɢ ᴛʜᴀᴛ ʙᴀʙʏ🖤.")

        kang_file = context.bot.get_file(file_id)
        if not is_animated:
            kang_file.download("kangsticker.png")
        else:
            kang_file.download("kangsticker.tgs")

        if args:
            sticker_emoji = str(args[0])
        elif msg.reply_to_message.sticker and msg.reply_to_message.sticker.emoji:
            sticker_emoji = msg.reply_to_message.sticker.emoji
        else:
            sticker_emoji = "🙂"

        if not is_animated:
            try:
                im = Image.open(kangsticker)
                maxsize = (512, 512)
                if (im.width and im.height) < 512:
                    size1 = im.width
                    size2 = im.height
                    if im.width > im.height:
                        scale = 512 / size1
                        size1new = 512
                        size2new = size2 * scale
                    else:
                        scale = 512 / size2
                        size1new = size1 * scale
                        size2new = 512
                    size1new = math.floor(size1new)
                    size2new = math.floor(size2new)
                    sizenew = (size1new, size2new)
                    im = im.resize(sizenew)
                else:
                    im.thumbnail(maxsize)
                if not msg.reply_to_message.sticker:
                    im.save(kangsticker, "PNG")
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    png_sticker=open("kangsticker.png", "rb"),
                    emojis=sticker_emoji,
                )
                edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="ᴠɪᴇᴡ ᴘᴀᴄᴋ", url=f"t.me/addstickers/{packname}"
                            )
                        ]
                    ]
                )
                msg.reply_text(
                    f"<b>ʏᴏᴜʀ ꜱᴛɪᴄᴋᴇʀ ʜᴀꜱ ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ʙᴀʙʏ🖤!</b>"
                    f"\nᴇᴍᴏᴊɪ ɪꜱ : {sticker_emoji}",
                    reply_markup=edited_keyboard,
                    parse_mode=ParseMode.HTML,
                )

            except OSError as e:

                print(e)
                return

            except TelegramError as e:
                if e.message == "Stickerset_invalid":
                    makepack_internal(
                        update,
                        context,
                        msg,
                        user,
                        sticker_emoji,
                        packname,
                        packnum,
                        png_sticker=open("kangsticker.png", "rb"),
                    )
                    
                elif e.message == "Sticker_png_dimensions":
                    im.save(kangsticker, "PNG")
                    context.bot.add_sticker_to_set(
                        user_id=user.id,
                        name=packname,
                        png_sticker=open("kangsticker.png", "rb"),
                        emojis=sticker_emoji,
                    )
                    edited_keyboard = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="ᴠɪᴇᴡ ᴘᴀᴄᴋ", url=f"t.me/addstickers/{packname}"
                                )
                            ]
                        ]
                    )
                    msg.reply_text(
                        f"<b>ʏᴏᴜʀ ꜱᴛɪᴄᴋᴇʀ ʜᴀꜱ ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ʙᴀʙʏ🖤!</b>"
                        f"\nᴇᴍᴏᴊɪ ɪꜱ : {sticker_emoji}",
                        reply_markup=edited_keyboard,
                        parse_mode=ParseMode.HTML,
                    )
                elif e.message == "Invalid sticker emojis":
                    msg.reply_text("ɪɴᴠᴀʟɪᴅ ᴇᴍᴏᴊɪ(s) ʙᴀʙʏ🖤.")
                elif e.message == "Stickers_too_much":
                    msg.reply_text("ᴍᴀx ᴘᴀᴄᴋꜱɪᴢᴇ ʀᴇᴀᴄʜᴇᴅ. ᴘʀᴇꜱꜱ ꜰ ᴛᴏ ᴘᴀʏ ʀᴇꜱᴘᴇᴄᴄ ʙᴀʙʏ🖤.")
                elif e.message == "Internal Server Error: sticker set not found (500)":
                    edited_keyboard = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="ᴠɪᴇᴡ ᴘᴀᴄᴋ", url=f"t.me/addstickers/{packname}"
                                )
                            ]
                        ]
                    )
                    msg.reply_text(
                        f"<b>ʏᴏᴜʀ ꜱᴛɪᴄᴋᴇʀ ʜᴀꜱ ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ʙᴀʙʏ🖤!</b>"
                        f"\nᴇᴍᴏᴊɪ ɪꜱ : {sticker_emoji}",
                        reply_markup=edited_keyboard,
                        parse_mode=ParseMode.HTML,
                    )
                print(e)

        else:
            packname = "animated" + str(user.id) + "_by_" + context.bot.username
            packname_found = 0
            max_stickers = 50
            while packname_found == 0:
                try:
                    stickerset = context.bot.get_sticker_set(packname)
                    if len(stickerset.stickers) >= max_stickers:
                        packnum += 1
                        packname = (
                            "animated"
                            + str(packnum)
                            + "_"
                            + str(user.id)
                            + "_by_"
                            + context.bot.username
                        )
                    else:
                        packname_found = 1
                except TelegramError as e:
                    if e.message == "Stickerset_invalid":
                        packname_found = 1
            try:
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    tgs_sticker=open("kangsticker.tgs", "rb"),
                    emojis=sticker_emoji,
                )
                edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="ᴠɪᴇᴡ ᴘᴀᴄᴋ", url=f"t.me/addstickers/{packname}"
                            )
                        ]
                    ]
                )
                msg.reply_text(
                    f"<b>ʏᴏᴜʀ ꜱᴛɪᴄᴋᴇʀ ʜᴀꜱ ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ʙᴀʙʏ🖤!</b>"
                    f"\nᴇᴍᴏᴊɪ ɪꜱ : {sticker_emoji}",
                    reply_markup=edited_keyboard,
                    parse_mode=ParseMode.HTML,
                )
            except TelegramError as e:
                if e.message == "Stickerset_invalid":
                    makepack_internal(
                        update,
                        context,
                        msg,
                        user,
                        sticker_emoji,
                        packname,
                        packnum,
                        tgs_sticker=open("kangsticker.tgs", "rb"),
                    )
                    
                elif e.message == "Invalid sticker emojis":
                    msg.reply_text("ɪɴᴠᴀʟɪᴅ ᴇᴍᴏᴊɪ(s) ʙᴀʙʏ🖤.")
                elif e.message == "Internal Server Error: sticker set not found (500)":
                    edited_keyboard = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="ᴠɪᴇᴡ ᴘᴀᴄᴋ", url=f"t.me/addstickers/{packname}"
                                )
                            ]
                        ]
                    )
                    msg.reply_text(
                        f"<b>ʏᴏᴜʀ ꜱᴛɪᴄᴋᴇʀ ʜᴀꜱ ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ʙᴀʙʏ🖤!</b>"
                        f"\nᴇᴍᴏᴊɪ ɪꜱ : {sticker_emoji}",
                        reply_markup=edited_keyboard,
                        parse_mode=ParseMode.HTML,
                    )
                print(e)

    elif args:
        try:
            try:
                urlemoji = msg.text.split(" ")
                png_sticker = urlemoji[1]
                sticker_emoji = urlemoji[2]
            except IndexError:
                sticker_emoji = "🙃"
            urllib.urlretrieve(png_sticker, kangsticker)
            im = Image.open(kangsticker)
            maxsize = (512, 512)
            if (im.width and im.height) < 512:
                size1 = im.width
                size2 = im.height
                if im.width > im.height:
                    scale = 512 / size1
                    size1new = 512
                    size2new = size2 * scale
                else:
                    scale = 512 / size2
                    size1new = size1 * scale
                    size2new = 512
                size1new = math.floor(size1new)
                size2new = math.floor(size2new)
                sizenew = (size1new, size2new)
                im = im.resize(sizenew)
            else:
                im.thumbnail(maxsize)
            im.save(kangsticker, "PNG")
            msg.reply_photo(photo=open("kangsticker.png", "rb"))
            context.bot.add_sticker_to_set(
                user_id=user.id,
                name=packname,
                png_sticker=open("kangsticker.png", "rb"),
                emojis=sticker_emoji,
            )
            edited_keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="ᴠɪᴇᴡ ᴘᴀᴄᴋ", url=f"t.me/addstickers/{packname}"
                        )
                    ]
                ]
            )
            msg.reply_text(
                f"<b>ʏᴏᴜʀ ꜱᴛɪᴄᴋᴇʀ ʜᴀꜱ ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ʙᴀʙʏ🖤!</b>" f"\nᴇᴍᴏᴊɪ ɪꜱ : {sticker_emoji}",
                reply_markup=edited_keyboard,
                parse_mode=ParseMode.HTML,
            )
        except OSError as e:
            msg.reply_text("ɪ ᴄᴀɴ ᴏɴʟʏ ᴋᴀɴɢ ɪᴍᴀɢᴇꜱ ʙᴀʙʏ🖤.")
            print(e)
            return
        except TelegramError as e:
            if e.message == "Stickerset_invalid":
                makepack_internal(
                    update,
                    context,
                    msg,
                    user,
                    sticker_emoji,
                    packname,
                    packnum,
                    png_sticker=open("kangsticker.png", "rb"),
                )
                
            elif e.message == "Sticker_png_dimensions":
                im.save(kangsticker, "PNG")
                context.bot.add_sticker_to_set(
                    user_id=user.id,
                    name=packname,
                    png_sticker=open("kangsticker.png", "rb"),
                    emojis=sticker_emoji,
                )
                edited_keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="ᴠɪᴇᴡ ᴘᴀᴄᴋ", url=f"t.me/addstickers/{packname}"
                            )
                        ]
                    ]
                )
                msg.reply_text(
                    f"<b>ʏᴏᴜʀ ꜱᴛɪᴄᴋᴇʀ ʜᴀꜱ ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ʙᴀʙʏ🖤!</b>"
                    f"\nᴇᴍᴏᴊɪ ɪꜱ : {sticker_emoji}",
                    reply_markup=edited_keyboard,
                    parse_mode=ParseMode.HTML,
                )
            elif e.message == "Invalid sticker emojis":
                msg.reply_text("ɪɴᴠᴀʟɪᴅ ᴇᴍᴏᴊɪ(s) ʙᴀʙʏ🖤.")
            elif e.message == "Stickers_too_much":
                msg.reply_text("ᴍᴀx ᴘᴀᴄᴋꜱɪᴢᴇ ʀᴇᴀᴄʜᴇᴅ. ᴘʀᴇꜱꜱ ꜰ ᴛᴏ ᴘᴀʏ ʀᴇꜱᴘᴇᴄᴄ ʙᴀʙʏ🖤.")
            elif e.message == "Internal Server Error: sticker set not found (500)":
                msg.reply_text(
                    f"<b>ʏᴏᴜʀ ꜱᴛɪᴄᴋᴇʀ ʜᴀꜱ ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ʙᴀʙʏ🖤!</b>"
                    f"\nᴇᴍᴏᴊɪ ɪꜱ : {sticker_emoji}",
                    reply_markup=edited_keyboard,
                    parse_mode=ParseMode.HTML,
                )
            print(e)
    else:
        packs_text = "*ᴘʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ꜱᴛɪᴄᴋᴇʀ, ᴏʀ ɪᴍᴀɢᴇ ᴛᴏ ᴋᴀɴɢ ɪᴛ ʙᴀʙʏ🖤!*\n"
        if packnum > 0:
            firstpackname = "a" + str(user.id) + "_by_" + context.bot.username
            for i in range(0, packnum + 1):
                if i == 0:
                    packs = f"t.me/addstickers/{firstpackname}"
                else:
                    packs = f"t.me/addstickers/{packname}"
        else:
            packs = f"t.me/addstickers/{packname}"

        edited_keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="ᴠɪᴇᴡ ᴘᴀᴄᴋ", url=f"{packs}")]]
        )
        msg.reply_text(
            packs_text, reply_markup=edited_keyboard, parse_mode=ParseMode.MARKDOWN
        )
    if os.path.isfile("kangsticker.png"):
        os.remove("kangsticker.png")
    elif os.path.isfile("kangsticker.tgs"):
        os.remove("kangsticker.tgs")


def makepack_internal(
    update,
    context,
    msg,
    user,
    emoji,
    packname,
    packnum,
    png_sticker=None,
    tgs_sticker=None,
):
    name = user.first_name
    name = name[:50]
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="ᴠɪᴇᴡ ᴘᴀᴄᴋ", url=f"{packname}")]]
    )
    try:
        extra_version = ""
        if packnum > 0:
            extra_version = " " + str(packnum)
        if png_sticker:
            sticker_pack_name = (
                f"{name}'s stic-pack (@{context.bot.username}) ʙᴀʙʏ🖤" + extra_version
            )
            success = context.bot.create_new_sticker_set(
                user.id,
                packname,
                sticker_pack_name,
                png_sticker=png_sticker,
                emojis=emoji,
            )
        if tgs_sticker:
            sticker_pack_name = (
                f"{name}'s ᴀɴɪ-ᴘᴀᴄᴋ (@{context.bot.username}) ʙᴀʙʏ🖤" + extra_version
            )
            success = context.bot.create_new_sticker_set(
                user.id,
                packname,
                sticker_pack_name,
                tgs_sticker=tgs_sticker,
                emojis=emoji,
            )

    except TelegramError as e:
        print(e)
        if e.message == "Sticker set name is already occupied":
            msg.reply_text(
                "<b>ʏᴏᴜʀ ꜱᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴄʀᴇᴀᴛᴇᴅ ʙᴀʙʏ🖤!</b>"
                "\n\nʏᴏᴜ ᴄᴀɴ ɴᴏᴡ ʀᴇᴘʟʏ ᴛᴏ ɪᴍᴀɢᴇꜱ, ꜱᴛɪᴄᴋᴇʀꜱ ᴀɴᴅ ᴀɴɪᴍᴀᴛᴇᴅ ꜱᴛɪᴄᴋᴇʀ ᴡɪᴛʜ /steal ᴛᴏ ᴀᴅᴅ ᴛʜᴇᴍ ᴛᴏ ʏᴏᴜʀ ᴘᴀᴄᴋ"
                "\n\n<b>ꜱᴇɴᴅ /stickers ᴛᴏ ꜰɪɴᴅ ᴀɴʏ ꜱᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ.</b>",
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML,
            )
        elif e.message == "Peer_id_invalid" or "bot was blocked by the user":
            msg.reply_text(
                f"{context.bot.first_name} ᴡᴀꜱ ʙʟᴏᴄᴋᴇᴅ ʙʏ ʏᴏᴜ ʙᴀʙʏ🖤.",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="ᴜɴʙʟᴏᴄᴋ", url=f"t.me/{context.bot.username}"
                            )
                        ]
                    ]
                ),
            )
        elif e.message == "Internal Server Error: created sticker set not found (500)":
            msg.reply_text(
                "<b>ʏᴏᴜʀ ꜱᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ ʜᴀꜱ ʙᴇᴇɴ ᴄʀᴇᴀᴛᴇᴅ ʙᴀʙʏ🖤!</b>"
                "\n\nʏᴏᴜ ᴄᴀɴ ɴᴏᴡ ʀᴇᴘʟʏ ᴛᴏ ɪᴍᴀɢᴇꜱ, ꜱᴛɪᴄᴋᴇʀꜱ ᴀɴᴅ ᴀɴɪᴍᴀᴛᴇᴅ ꜱᴛɪᴄᴋᴇʀ ᴡɪᴛʜ /steal ᴛᴏ ᴀᴅᴅ ᴛʜᴇᴍ ᴛᴏ ʏᴏᴜʀ ᴘᴀᴄᴋ"
                "\n\n<b>ꜱᴇɴᴅ /stickers ᴛᴏ ꜰɪɴᴅ ꜱᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ.</b>",
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML,
            )
        return

    if success:
        msg.reply_text(
            "<b>ʏᴏᴜʀ ꜱᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ ʜᴀꜱ ʙᴇᴇɴ ᴄʀᴇᴀᴛᴇᴅ ʙᴀʙʏ🖤!</b>"
            "\n\nʏᴏᴜ ᴄᴀɴ ɴᴏᴡ ʀᴇᴘʟʏ ᴛᴏ ɪᴍᴀɢᴇꜱ, ꜱᴛɪᴄᴋᴇʀꜱ ᴀɴᴅ ᴀɴɪᴍᴀᴛᴇᴅ ꜱᴛɪᴄᴋᴇʀ ᴡɪᴛʜ /steal ᴛᴏ ᴀᴅᴅ ᴛʜᴇᴍ ᴛᴏ ʏᴏᴜʀ ᴘᴀᴄᴋ"
            "\n\n<b>ꜱᴇɴᴅ /stickers ᴛᴏ ꜰɪɴᴅ ꜱᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ.</b>",
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
        )
    else:
        msg.reply_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ᴄʀᴇᴀᴛᴇ ꜱᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ. ᴘᴏꜱꜱɪʙʟʏ ᴅᴜᴇ ᴛᴏ ʙʟᴇᴋ ᴍᴇᴊɪᴋ ʙᴀʙʏ🖤.")


def getsticker(update, context):
    msg = update.effective_message
    chat_id = update.effective_chat.id
    if msg.reply_to_message and msg.reply_to_message.sticker:
        context.bot.sendChatAction(chat_id, "typing")
        update.effective_message.reply_text(
            "ʜᴇʏ"
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", ᴘʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ ꜰɪʟᴇ ʏᴏᴜ ʀᴇQᴜᴇꜱᴛᴇᴅ ʙᴇʟᴏᴡ ʙᴀʙʏ🖤."
            "\nᴘʟᴇᴀꜱᴇ ᴜꜱᴇ ᴛʜɪꜱ ꜰᴇᴀᴛᴜʀᴇ ᴡɪꜱᴇʟʏ!",
            parse_mode=ParseMode.HTML,
        )
        context.bot.sendChatAction(chat_id, "upload_document")
        file_id = msg.reply_to_message.sticker.file_id
        newFile = context.bot.get_file(file_id)
        newFile.download("sticker.png")
        context.bot.sendDocument(chat_id, document=open("sticker.png", "rb"))
        context.bot.sendChatAction(chat_id, "upload_photo")
        context.bot.send_photo(chat_id, photo=open("sticker.png", "rb"))

    else:
        context.bot.sendChatAction(chat_id, "typing")
        update.effective_message.reply_text(
            "ʜᴇʏ"
            + f"{mention_html(msg.from_user.id, msg.from_user.first_name)}"
            + ", ᴘʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴛᴏ ꜱᴛɪᴄᴋᴇʀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ɢᴇᴛ ꜱᴛɪᴄᴋᴇʀ ɪᴍᴀɢᴇ ʙᴀʙʏ🖤",
            parse_mode=ParseMode.HTML,
        )


def cb_sticker(update: Update, context: CallbackContext):
    msg = update.effective_message
    split = msg.text.split(" ", 1)
    if len(split) == 1:
        msg.reply_text("ᴘʀᴏᴠɪᴅᴇ ꜱᴏᴍᴇ ɴᴀᴍᴇ ᴛᴏ ꜱᴇᴀʀᴄʜ ꜰᴏʀ ᴘᴀᴄᴋ ʙᴀʙʏ🖤.")
        return

    scraper = cloudscraper.create_scraper()
    text = scraper.get(combot_stickers_url + split[1]).text
    soup = bs(text, "lxml")
    results = soup.find_all("a", {"class": "sticker-pack__btn"})
    titles = soup.find_all("div", "sticker-pack__title")
    if not results:
        msg.reply_text("No results found :(.")
        return
    reply = f"ꜱᴛɪᴄᴋᴇʀꜱ ꜰᴏʀ *{split[1]}* ʙᴀʙʏ🖤:"
    for result, title in zip(results, titles):
        link = result["href"]
        reply += f"\n• [{title.get_text()}]({link})"
    msg.reply_text(reply, parse_mode=ParseMode.MARKDOWN)


def getsticker(update: Update, context: CallbackContext):
    bot = context.bot
    msg = update.effective_message
    chat_id = update.effective_chat.id
    if msg.reply_to_message and msg.reply_to_message.sticker:
        file_id = msg.reply_to_message.sticker.file_id
        new_file = bot.get_file(file_id)
        new_file.download("sticker.png")
        bot.send_document(chat_id, document=open("sticker.png", "rb"))
        os.remove("sticker.png")
    else:
        update.effective_message.reply_text(
            "ᴘʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ꜱᴛɪᴄᴋᴇʀ ꜰᴏʀ ᴍᴇ ᴛᴏ ᴜᴘʟᴏᴀᴅ ɪᴛꜱ ᴘɴɢ ʙᴀʙʏ🖤."
        )


def delsticker(update, context):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.sticker:
        file_id = msg.reply_to_message.sticker.file_id
        context.bot.delete_sticker_from_set(file_id)
        msg.reply_text("Deleted!")
    else:
        update.effective_message.reply_text(
            "ᴘʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴛᴏ ꜱᴛɪᴄᴋᴇʀ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴅᴇʟ ꜱᴛɪᴄᴋᴇʀ ʙᴀʙʏ🖤"
        )

__mod_name__ = "Stickers"

__help__ = """
*Help menu for stickers tools*

» `/stickerid`*:* ʀᴇᴘʟʏ ᴛᴏ ᴀ ꜱᴛɪᴄᴋᴇʀ ᴛᴏ ᴍᴇ ᴛᴏ ᴛᴇʟʟ ʏᴏᴜ ɪᴛꜱ ꜰɪʟᴇ ɪᴅ.
» `/getsticker`*:* ʀᴇᴘʟʏ ᴛᴏ ᴀ ꜱᴛɪᴄᴋᴇʀ ᴛᴏ ᴍᴇ ᴛᴏ ᴜᴘʟᴏᴀᴅ ɪᴛꜱ ʀᴀᴡ ᴘɴɢ ꜰɪʟᴇ.
» `/kang`*:* ʀᴇᴘʟʏ ᴛᴏ ᴀ ꜱᴛɪᴄᴋᴇʀ ᴛᴏ ᴀᴅᴅ ɪᴛ ᴛᴏ ʏᴏᴜʀ ᴘᴀᴄᴋ.
» `/delsticker`*:* ʀᴇᴘʟʏ ᴛᴏ ʏᴏᴜʀ ᴀɴɪᴍᴇ ᴇxɪꜱᴛ ꜱᴛɪᴄᴋᴇʀ ᴛᴏ ʏᴏᴜʀ ᴘᴀᴄᴋ ᴛᴏ ᴅᴇʟᴇᴛᴇ ɪᴛ.
» `/stickers`*:* ꜰɪɴᴅ ꜱᴛɪᴄᴋᴇʀꜱ ꜰᴏʀ ɢɪᴠᴇɴ ᴛᴇʀᴍ ᴏɴ ᴄᴏᴍʙᴏᴛ ꜱᴛɪᴄᴋᴇʀ ᴄᴀᴛᴀʟᴏɢᴜᴇ
» `/tiny`*:* ᴛᴏ ᴍᴀᴋᴇ ꜱᴍᴀʟʟ ꜱᴛɪᴄᴋᴇʀ
» `/kamuii` <1-8> *:* ᴛᴏ ᴅᴇᴇᴘᴇꜰʏɪɴɢ ꜱᴛɪᴋᴇʀ
» `/mmf` <ʀᴇᴘʟʏ ᴡɪᴛʜ ᴛᴇxᴛ>*:* ᴛᴏ ᴅʀᴀᴡ ᴀ ᴛᴇxᴛ ꜰᴏʀ ꜱᴛɪᴄᴋᴇʀ ᴏʀ ᴘᴏʜᴏᴛꜱ
"""


STICKERID_HANDLER = DisableAbleCommandHandler("stickerid", stickerid, run_async=True)
GETSTICKER_HANDLER = DisableAbleCommandHandler("getsticker", getsticker, run_async=True)
KANG_HANDLER = DisableAbleCommandHandler("kang", kang, pass_args=True, run_async=True)
DEL_HANDLER = DisableAbleCommandHandler("delsticker", delsticker, run_async=True)
STICKERS_HANDLER = DisableAbleCommandHandler("stickers", cb_sticker, run_async=True)

dispatcher.add_handler(STICKERS_HANDLER)
dispatcher.add_handler(STICKERID_HANDLER)
dispatcher.add_handler(GETSTICKER_HANDLER)
dispatcher.add_handler(KANG_HANDLER)
dispatcher.add_handler(DEL_HANDLER)
