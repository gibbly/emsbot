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






async def getstate():
        try:
            state = requests.get('https://ems.isitdoneyet.co.uk/api/key/active', auth=(USER, PASS))
        except:
            print("there was an error fetching the current state" + str(state))
        state = json.loads(state.text)
        return state

async def updatenowplaying():

    state = await getstate()
    try:
        member = guild.get_member(int(state['nick']))
        name = member.display_name
        usericon = member.avatar_url_as(format=None, static_format="jpg")
        usericon = str(str(usericon).split('?')[0])

    except:
        name = state['nick']
        usericon = ''
        print(str(state['nick']) + "is not a visible discord id, using raw value instead")



    customdescription = "Custom descriptions coming soon :tm:"
    streamthumbnail = 'https://cdn.discordapp.com/attachments/758341897453437049/758342103779901440/EMS.png'
    customurl = ''



    global laststreamer
    if name != laststreamer:
        laststreamer = name
        try:
            if state.get("priority") >= 10:
                embed=discord.Embed(title="watch " + name + " LIVE NOW!", url="https://www.youtube.com/channel/UCJZX0lhyQyicb9nVDS8R40w/live", description=customdescription)
                embed.set_author(name=name, url=customurl,icon_url=usericon)
                embed.set_thumbnail(url=streamthumbnail)
                embed.set_footer(text="brought to you by ems ;)")
                await channel.send(embed=embed)
                await channel.send('<@&' + str(ping) + '>')
            else:
                embed=discord.Embed(title="Now playing: " + name, url="https://www.youtube.com/channel/UCJZX0lhyQyicb9nVDS8R40w/live", description=customdescription)
                embed.set_author(name= name, url=customurl,icon_url=usericon)
                embed.set_thumbnail(url=streamthumbnail)
                embed.set_footer(text="brought to you by ems ;)")
                await channel.send(embed=embed)
        except:
            print()


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    global guild
    guild = bot.get_guild(guildid)
    print(guild)
    global channel
    channel = bot.get_channel(channelid)
    while 1==1:
        try:
            await updatenowplaying()
            await asyncio.sleep(30)
        except:
            print("status update failed")
            await asyncio.sleep(90)



@bot.event
async def on_message(message):
    global botid
    if str(message.channel) == "now-playing" and message.author.id != int(botid) :
        await asyncio.sleep(3)
        await message.channel.purge(limit=1)
    await bot.process_commands(message)

@bot.command(name='refresh', help='manually fetches now playing data', cat='debug')
async def refresh(ctx):

        await updatenowplaying()













bot.run(TOKEN)
