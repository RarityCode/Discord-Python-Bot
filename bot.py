import discord
from discord.ext import commands
import botconfig

#hi= 'Добро пожаловать на сервер '+member+'!'
#bye= 'Мы будем скучать '+member+'!'
bot=commands.Bot(command_prefix='!')
client=discord.Client()
SMchannel=discord.Guild.system_channel

@bot.event
async def on_ready():
    print('logged on')

@client.event
async def on_member_join(member):
    print('1')
    hi = 'Добро пожаловать {}, на сервер {}!'.format(member.mention, server.name)
    #await client.send_message(SMchannel, hi)
    await SMchannel.send(hi)

#async def on_member_remove(member):
#CODE

bot.run(botconfig.TOKEN)