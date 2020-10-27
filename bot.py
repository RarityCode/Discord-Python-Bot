from discord import Intents
from discord.ext.commands import Bot
import botconfig

intents = Intents(members=True, guilds=True, messages=True)
bot = Bot(command_prefix='!', intents=intents)  # bot prefix for later use
target = ""


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


@bot.command()
async def emoji_counting(ctx, arg):
    if arg == 'on':
        # ON CODE
        await ctx.send(f'Подсчёт включён, {ctx.message.author.mention}.')
    if arg == 'off':
        # OFF CODE
        await ctx.send(f'Подсчёт выключён, {ctx.message.author.mention}.')


@bot.command()
async def fireban(ctx, arg):  # setting the target of reactions
    global target
    target = arg
    await ctx.send(f'Жертвой выбран {arg}.')


@bot.event
async def on_message(message):  # posts determined reaction on all posts of defined user
    await bot.process_commands(message)  # without this on_message breaks bot.commands
    if message.author.name == target:
        await message.add_reaction('✅')


if __name__ == "__main__":
    bot.run(botconfig.TOKEN)
