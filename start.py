import os
import random
import json
import aiohttp
import asyncio
import time
import discord
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
USER = os.getenv('user')
PASS = os.getenv('pass')

intents = discord.Intents.default()
intents.members = True
botid = int(os.getenv('BOT_ID'))
bot = commands.Bot(command_prefix='+', intents = intents)



default = {
"usericon": "https://cdn.discordapp.com/embed/avatars/0.png",
"nicklink": "",
"color": 0x1e2936,
"overridediscord": False,
"streamthumbnail": "https://cdn.discordapp.com/attachments/758341897453437049/758342103779901440/EMS.png",
"streamdescription": "no u",
"extraimage": "",
"priority": "10",
}



async def activeget():
    try:
        err = "the state could not be fetched"
        auth = aiohttp.BasicAuth(USER, PASS)
        async with aiohttp.request('GET', 'https://ems.isitdoneyet.co.uk/api/key/active', auth=auth) as r:
            if r.status == 200 and r.content_type == 'application/json':
                state = await r.json()

                if 'discord_id' in state:
                    pass
                else:
                    state["discord_id"] = 0
                return state
            else:
                err = await r.text()
    except:
        print("there was an error fetching the current state" + err)
        return{"nick": "error", "priority": "10"}


async def userdataget(discord_id):
    return {"streamdescription": "Custom descriptions coming soon :tm:"}

async def generatecard(user):
    trashvalue = {}
    trashvalue.update(default)
    trashvalue.update(user)
    user = trashvalue
    user.update(await userdataget(user.get("discord_id")))
    embed = discord.Embed(title="", url="", description=user.get("streamdescription"), colour=discord.Colour(user.get("color")))
    embed.set_image(url=user.get("extraimage"))
    embed.set_thumbnail(url=user.get("streamthumbnail"))
    if user.get("overridediscord") == "TRUE":
        embed.set_author(name=user.get("nick"), url=user.get("nicklink"), icon_url=user.get("usericon"))
    else:
        try:
            member = guild.get_member(int(user.get("discord_id")))
            name = member.display_name
            usericon = member.avatar_url_as(format=None, static_format="jpg")
            usericon = str(str(usericon).split('?')[0])
        except:
            name = user.get("nick")
            usericon = user.get("usericon")
            print(str(user) + "discord user data scrape failed? falling back to nick")
        embed.set_author(name=name, url=user.get("nicklink"), icon_url=usericon)
    return embed


async def streamercard(user):
    embed = await generatecard(user)
    embed.add_field(name="Watch on", value="[**[Twitch]**](http://twitch.tv/earthmodularsociety) [**[YouTube]**](http://youtube.com/c/EarthModularSociety/live)")
    embed.add_field(name="Don't forget to check out the site!", value="http://earthmodularsociety.com/", inline=False)
    embed.set_footer(text="Brought to you by EMS ;)", icon_url="https://cdn.discordapp.com/attachments/758341897453437049/758342103779901440/EMS.png")
    return embed










@bot.event
async def on_message(message):
    if message.webhook_id != None:
        if message.content == "blorp":
            user = await activeget()
            embed = await streamercard(user)
            if int(user.get("priority")) >= 10:
                content = "Come watch " + user.get("nick") + " LIVE " + str(ping.mention)
            else:
                content = ""
            await channel.send(embed=embed, content=content)

#        elif message.content[0] == "+":
#            if message.content.startswith["+nowplaying"]:
#                await nowplaying()
#
#
#
#
#async def card(ctx, *, arg):
#
#    arg = arg[2:-1]
#    user = {"discord_id": arg}
#    embed = await generatecard(user)
#    await channel.send(embed=embed)
#
#
#async def nowplaying():
#    user = await activeget()
#    embed = await streamercard(user)
#    if user.get("priority") >= 10:
#        content = "Come watch " + user.get("nick") + " LIVE " + str(ping.mention)
#    else:
#        content = ""
#    await channel.send(embed=embed, content=content)
#
#
#async def ping(ctx):
#	print("ping'd")
#	await ctx.channel.send("pong")
#


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


    global guild
    guild = int(os.getenv('DISCORD_GUILD'))
    guild = bot.get_guild(guild)
    print(guild)

    global channel
    channel = int(os.getenv('DISCORD_CHANNEL'))
    channel = bot.get_channel(channel)
    print(channel)

    global ping
    ping = intgos.getenv('PING_ROLE_ID'))
    ping = guild.get_role(ping)
    print(ping)


















bot.run(TOKEN)
