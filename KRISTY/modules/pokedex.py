import aiohttp
from pyrogram import filters
from KRISTY import pbot as tomori


@tomori.on_message(filters.command("pokedex"))
async def PokeDex(_, message):
    if len(message.command) != 2:
        await message.reply_text("/pokedex ᴘᴏᴋᴇᴍᴏɴ ɴᴀᴍᴇ ʙᴀʙʏ🖤")
        return
    pokemon = message.text.split(None, 1)[1]
    pokedex = f"https://some-random-api.ml/pokedex?pokemon={pokemon}"
    async with aiohttp.ClientSession() as session:
        async with session.get(pokedex) as request:
            if request.status == 404:
                return await message.reply_text("ᴡʀᴏɴɢ ᴘᴏᴋᴇᴍᴏɴ ɴᴀᴍᴇ ʙᴀʙʏ🖤")

            result = await request.json()
            try:
                pokemon = result["name"]
                pokedex = result["id"]
                type = result["type"]
                poke_img = f"https://img.pokemondb.net/artwork/large/{pokemon}.jpg"
                abilities = result["abilities"]
                height = result["height"]
                weight = result["weight"]
                gender = result["gender"]
                stats = result["stats"]
                description = result["description"]
                caption = f"""
**ᴘᴏᴋᴇᴍᴏɴ:** `{pokemon}`
**ᴘᴏᴋᴇᴅᴇx:** `{pokedex}`
**ᴛʏᴘᴇ:** `{type}`
**ᴀʙɪʟɪᴛɪᴇꜱ:** `{abilities}`
**ʜᴇɪɢʜᴛ:** `{height}`
**ᴡᴇɪɢʜᴛ:** `{weight}`
**ɢᴇɴᴅᴇʀ:** `{gender}`
**ꜱᴛᴀᴛꜱ:** `{stats}`
**ᴅᴇꜱᴄʀɪᴘᴛɪᴏɴ:** `{description}`"""
            except Exception as e:
                print(str(e))
                pass
    await message.reply_photo(photo=poke_img, caption=caption)


