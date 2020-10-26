from discord import Intents, Guild
from discord.ext.commands import Bot
import botconfig

intents = Intents(members=True, guilds=True)
bot = Bot(command_prefix='!', intents=intents)  # bot prefix for later use

@bot.event
async def on_ready():
    print('logged on')

@bot.event
async def on_member_join(member):  # greetings
    hi = 'Добро пожаловать {}, на сервер {}!'.format(member.mention, member.guild.name)
    await member.guild.system_channel.send(hi)
@bot.event
async def on_member_remove(member):  # farewells
    bye = 'Прощай {}, мы будем скучать.'.format(member.mention)
    await member.guild.system_channel.send(bye)

if __name__ == "__main__":
    bot.run(botconfig.TOKEN)