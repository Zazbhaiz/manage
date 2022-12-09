from pyrogram import filters

from KRISTY import pbot as app, arq
from KRISTY.utils.errors import capture_err

__mod_name__ = "Reddit"

__help__ = """
 » `/Reddit`<text> :  ɢɪᴠᴇꜱ ʀᴇᴘʟʏ ʀᴇʟᴀᴛᴇᴅ ᴛᴏ ᴛᴇxᴛ.
 """


@app.on_message(filters.command("reddit") & ~filters.edited)
@capture_err
async def reddit(_, message):
    if len(message.command) != 2:
        return await message.reply_text("/reddit ɴᴇᴇᴅꜱ ᴀɴ ᴀʀɢᴜᴍᴇɴᴛ ʙᴀʙʏ🖤.")
    subreddit = message.text.split(None, 1)[1]
    m = await message.reply_text("ꜱᴇᴀʀᴄʜɪɴɢ...")
    reddit = await arq.reddit(subreddit)
    if not reddit.ok:
        return await m.edit(reddit.result)
    reddit = reddit.result
    nsfw = reddit.nsfw
    sreddit = reddit.subreddit
    title = reddit.title
    image = reddit.url
    link = reddit.postLink
    if nsfw:
        return await m.edit("ɴꜱꜰᴡ ʀᴇꜱᴜʟᴛꜱ ᴄᴏᴜʟᴅ ɴᴏᴛ ʙᴇ ꜱʜᴏᴡɴ ʙᴀʙʏ🖤.")
    caption = f"""
**Title:** `{title}`
**Subreddit:** {sreddit}
**PostLink:** {link}"""
    try:
        await message.reply_photo(photo=image, caption=caption)
        await m.delete()
    except Exception as e:
        await m.edit(e.MESSAGE)
