import os
import re

import requests
from bs4 import BeautifulSoup
from telethon import events

from KRISTY import telethn as tbot

@tbot.on(events.NewMessage(pattern="^/book (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    lool = 0
    KkK = await event.reply("`ꜱᴇᴀʀᴄʜɪɴɢ ꜰᴏʀ ᴛʜᴇ ʙᴏᴏᴋ ʙᴀʙʏ🖤...`")
    lin = "https://b-ok.cc/s/"
    text = input_str
    link = lin + text

    headers = [
        "User-Agent",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0",
    ]
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    f = open("book.txt", "w")
    total = soup.find(class_="totalCounter")
    for nb in total.descendants:
        nbx = nb.replace("(", "").replace(")", "")
    if nbx == "0":
        await event.reply("ɴᴏ ʙᴏᴏᴋꜱ ꜰᴏᴜɴᴅ ᴡɪᴛʜ ᴛʜᴀᴛ ɴᴀᴍᴇ ʙᴀʙʏ🖤.")
    else:

        for tr in soup.find_all("td"):
            for td in tr.find_all("h3"):
                for ts in td.find_all("a"):
                    title = ts.get_text()
                    lool = lool + 1
                for ts in td.find_all("a", attrs={"href": re.compile("^/book/")}):
                    ref = ts.get("href")
                    link = "https://b-ok.cc" + ref

                f.write("\n" + title)
                f.write("\nʙᴏᴏᴋ ʟɪɴᴋ:- " + link + "\n\n")

        f.write("By KʀɪsTʏ.")
        f.close()
        caption = "ᴊᴏɪɴ ꜱᴜᴘᴘᴏʀᴛ @kristy_af"

        await tbot.send_file(
            event.chat_id,
            "book.txt",
            caption=f"**ʙᴏᴏᴋꜱ ɢᴀᴛʜᴇʀᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʙᴀʙʏ🖤!**",
        )
        os.remove("book.txt")
        await KkK.delete()

__help__ = """
** book  **
 ❍ /book  <book name > : ꜱᴇᴀʀᴄʜ ᴀɴʏ ʙᴏᴏᴋ ᴜꜱᴇɪɴɢ ᴛʜɪꜱ ʙᴏᴛ  
"""
__mod_name__ = "Book"
