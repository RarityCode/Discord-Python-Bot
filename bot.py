import discord
from discord.ext import commands
import botconfig

bot=commands.Bot(command_prefix='!') # bot prefix for later use
client=discord.Client()
SMchannel=discord.Guild.system_channel

@bot.event
async def on_ready():
    print('logged on')

@client.event
async def on_member_join(member):
    print('1')
    hi = 'Добро пожаловать {}, на сервер {}!'.format(member.mention, server.name)
    await SMchannel.send(hi)
async def on_member_remove(member):
    print('2')
    bye = 'Прощай {}, мы будем скучать.'.format(member.mention)
    await SMchannel.send(bye)

bot.run(botconfig.TOKEN)