import os
import random
import json
import requests
import asyncio
import time
import discord
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
USER = os.getenv('user')
PASS = os.getenv('pass')
guildid = int(os.getenv('DISCORD_GUILD'))
channelid = int(os.getenv('DISCORD_CHANNEL'))
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='+', intents = intents)
laststreamer = ''
ping = os.getenv('PING_ROLE_ID')
botid = int(os.getenv('BOT_ID'))









async def updatenowplaying():

    try:
        state = requests.get('https://ems.isitdoneyet.co.uk/api/key/active', auth=(USER, PASS))
        state = json.loads(state.text)
        if 'discord_id' in state:
            pass
        else:
            state["discord_id"] = 0

    except:
        print("there was an error fetching the current state" + str(state))

    if int(state.get('discord_id')) != 0 :
        try:
            member = guild.get_member(int(state['discord_id']))
            name = member.display_name
            usericon = member.avatar_url_as(format=None, static_format="jpg")
            usericon = str(str(usericon).split('?')[0])
        except:
            name = state['nick']
            usericon = ''
            print(str(state) + "invalid discord id")
    else:
        name = state['nick']
        usericon = ''
        print(name + ' has no discord id')

    customdescription = "Custom descriptions coming soon :tm:"
    streamthumbnail = 'https://cdn.discordapp.com/attachments/758341897453437049/758342103779901440/EMS.png'
    customurl = ''

    global laststreamer
    if name != laststreamer:
        try:
            if state.get("priority") >= 10:
                embed=discord.Embed(title="watch " + name + " LIVE NOW!", url="https://www.youtube.com/channel/UCJZX0lhyQyicb9nVDS8R40w/live", description=customdescription)
                embed.set_author(name=name, url=customurl,icon_url=usericon)
                embed.set_thumbnail(url=streamthumbnail)
                embed.set_footer(text="brought to you by ems ;)")
                await channel.send(embed=embed)
                await channel.send('<@&' + str(ping) + '>')
                channel2 = bot.get_channel(756541590494904321)
                await channel2.send(embed=embed)
            else:
                embed=discord.Embed(title="Now playing: " + name, url="https://www.youtube.com/channel/UCJZX0lhyQyicb9nVDS8R40w/live", description=customdescription)
                embed.set_author(name= name, url=customurl,icon_url=usericon)
                embed.set_thumbnail(url=streamthumbnail)
                embed.set_footer(text="brought to you by ems ;)")
                await channel.send(embed=embed)
                channel2 = bot.get_channel(756541590494904321)
                await channel2.send(embed=embed)
            laststreamer = name
        except:
            pass


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    global guild
    guild = bot.get_guild(guildid)
    print(guild)
    global channel
    channel = bot.get_channel(channelid)
    while True:
        try:
            await updatenowplaying()
        except:
            await asyncio.sleep(60)
        await asyncio.sleep(30)
















bot.run(TOKEN)
