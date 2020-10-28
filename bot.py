from discord import Intents
from discord.ext.commands import Bot, has_permissions, has_role
import botconfig

intents = Intents(members=True, guilds=True, messages=True)
bot = Bot(command_prefix='!', intents=intents)  # bot prefix for later use
target = ""
emote = ""
SystemChannel = ''


def check_sc():  # checking if SystemChannel is set
    global SystemChannel
    for user in bot.get_all_members():
        if user.id == botconfig.ID:
            if user.guild.system_channel is None:
                print('System channel not set.')
                return False
            else:
                SystemChannel = user.guild.system_channel
                return True


@bot.event
async def on_ready():
    print('logged on')
    if check_sc():
        await SystemChannel.send('Systems ready!')


@bot.event
async def on_member_join(member):  # greetings
    if check_sc():
        hi = 'Добро пожаловать {}, на сервер {}!'.format(member.mention, member.guild.name)
        await SystemChannel.send(hi)


@bot.event
async def on_member_remove(member):  # farewells
    if check_sc():
        bye = 'Прощай {}, мы будем скучать.'.format(member.mention)
        await SystemChannel.send(bye)


@bot.command()
async def emoji_counting(ctx, arg):
    if arg == 'on':
        # ON CODE
        await ctx.send(f'Подсчёт включён, {ctx.message.author.mention}.')
    if arg == 'off':
        # OFF CODE
        await ctx.send(f'Подсчёт выключён, {ctx.message.author.mention}.')


@bot.command()
@has_permissions(administrator=True)
async def fireban(ctx, arg, arg1):  # setting the target of reactions
    global target, emote
    target = arg
    emote = arg1
    await ctx.send(f'Жертвой выбран {arg}.')


@bot.event
async def on_message(message):  # posts determined reaction on all posts of defined user
    await bot.process_commands(message)  # without this on_message breaks bot.commands
    if message.author.name == target:
        await message.add_reaction(emote)


if __name__ == "__main__":
    bot.run(botconfig.TOKEN)
