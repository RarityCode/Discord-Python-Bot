import discord
from discord import Intents
from discord.ext.commands import Bot, has_permissions
from datetime import datetime
import botconfig

intents = Intents(members=True, guilds=True, messages=True, reactions=True)
bot = Bot(command_prefix='!', intents=intents)
bot.remove_command('help')
target = ""
target_server = ''
emote = ""
bye1 = 'So long '
bye2 = '.'
hi1 = 'Welcome '
hi2 = ' to '
hi3 = '!'


def emoji_sort(emoji):
    return emoji[1]


@bot.event
async def on_ready():
    print('logged on')
    status = discord.Activity(type=discord.ActivityType.listening,
                              name='your commands.\nType !help to receive full list of commands.')
    await bot.change_presence(activity=status)


@bot.event
async def on_member_join(member):  # greetings
    hi = f'{hi1}{member.mention}{hi2}{member.guild.name}{hi3}'
    await member.guild.system_channel.send(hi)


@bot.event
async def on_member_remove(member):  # farewells
    bye = f'{bye1}{member.mention}{bye2}'
    await member.guild.system_channel.send(bye)


@bot.event
async def on_message(message):  # posts defined reaction on all posts of defined user
    await bot.process_commands(message)  # without this on_message breaks bot.commands
    if message.author.mention == target and message.guild == target_server:
        await message.add_reaction(emote)


@bot.command()
@has_permissions(administrator=True)
async def reacts(ctx, arg, arg1):  # setting the target of reactions
    global target, emote, target_server
    target = arg.replace("@!", "@")  # for some reason ordinary mention and author.mention differ - ordinary mention includes exclamation mark
    target_server = ctx.guild
    emote = arg1
    await ctx.send(f'Жертвой выбран {target}.')


@bot.command()
@has_permissions(administrator=True)
async def help(ctx):
    post = discord.Embed(color=0x3D85C6)
    post.set_author(name='List of commands:')
    post.add_field(name='!reacts name emoji',
                   value='Bot will add reaction on every post of defined user.\nname - name of the target user\nemoji - emoji that bot will use',
                   inline=False)
    post.add_field(name='!emoji_counting',
                   value='Bot will count emoji used on server and in reactions, then will post statistic.', inline=False)
    post.add_field(name='!set_hi "text1" "text2" "text3"',
                   value='Bot will send a message when member joins the server.\ntext1 - text in quotation marks that will be placed before mentioning new member\ntext2 - text in quotation marks that will be placed between mention and your server name\ntext3 - text in quotation marks that will be placed after your server name',
                   inline=False)
    post.add_field(name='!set_bye "text1" "text2"',
                   value='Bot will send a message when member leaves the server.\ntext1 - text in quotation marks that will be placed before mentioning left member\ntext2 - text in quotation marks that will be placed after mentioning left member',
                   inline=False)
    await ctx.send(embed=post)


@bot.command()
@has_permissions(administrator=True)
async def set_hi(ctx, arg, arg1, arg2):
    global hi1, hi2, hi3
    hi1 = arg
    hi2 = arg1
    hi3 = arg2
    await ctx.send(f'Приветствие будет таким:\n{hi1}@username{hi2}@servername{hi3}')


@bot.command()
@has_permissions(administrator=True)
async def set_bye(ctx, arg, arg1):
    global bye1, bye2
    bye1 = arg
    bye2 = arg1
    await ctx.send(f'Прощание будет таким:\n{bye1}@username{bye2}')


@bot.command()
@has_permissions(administrator=True)
async def emoji_counting(ctx):
    date = datetime.now(tz=None).replace(day=1)
    date_month = date.month - 1
    date_year = date.year - 1
    if date_month < 1:
        date = date.replace(month=12, year=date_year)
    else:
        date = date.replace(month=date_month)
    reaction_counter = []
    for emoji in ctx.author.guild.emojis:  # list of custom emojis
        ctr = [emoji, 0]
        reaction_counter.append(ctr)
    for channel in bot.get_all_channels():  # cycle of messages on server
        if channel.type.name == 'text':
            messages = await channel.history(limit=None, after=date).flatten()
            for message in messages:
                if message.reactions.__len__ is not None:  # reaction counting
                    for reaction in message.reactions:
                        for counter in reaction_counter:
                            if counter[0] == reaction.emoji:
                                counter[1] = counter[1] + reaction.count
                for emoji in reaction_counter:  # emoji counting in text
                    string = ':' + emoji[0].name + ':'
                    if string in message.content:
                        emoji[1] = emoji[1] + 1
    reaction_counter.sort(key=emoji_sort)
    for emoji in reaction_counter:
        await ctx.send(f'{emoji[0]} - {emoji[1]}.')
        if emoji[1] <= 10:
            await emoji[0].delete(reason='Использовалась меньше десяти раз.')


if __name__ == "__main__":
    bot.run(botconfig.TOKEN)
