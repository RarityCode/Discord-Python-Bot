import discord
from discord import Intents
from discord.ext.commands import Bot, has_permissions
from datetime import datetime
import botconfig

intents = Intents(members=True, guilds=True, messages=True, reactions=True)
bot = Bot(command_prefix='!', intents=intents)
bot.remove_command('help')
target = ""
emote = ""
SystemChannel = ''
bye1 = ''
bye2 = ''
hi1 = ''
hi2 = ''
hi3 = ''


def emoji_sort(emoji):
    return emoji[1]


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
        status1 = discord.Activity(type=discord.ActivityType.listening,
                                   name='your commands.\nType !help to receive full list of commands.')
        await bot.change_presence(activity=status1)
    else:
        status2 = discord.Activity(type=discord.ActivityType.listening,
                                   name='your commands.\nType !help to receive full list of commands.\nWarning: System Channel not set, some features will not work.')
        await bot.change_presence(activity=status2)


@bot.event
async def on_member_join(member):  # greetings
    if check_sc():
        hi = f'{hi1}{member.mention}{hi2}{member.guild.name}{hi3}'
        await SystemChannel.send(hi)


@bot.event
async def on_member_remove(member):  # farewells
    if check_sc():
        bye = f'{bye1}{member.mention}{bye2}'
        await SystemChannel.send(bye)


@bot.event
async def on_message(message):  # posts defined reaction on all posts of defined user
    await bot.process_commands(message)  # without this on_message breaks bot.commands
    if message.author.mention == target:
        await message.add_reaction(emote)


@bot.command()
@has_permissions(administrator=True)
async def reacts(ctx, arg, arg1):  # setting the target of reactions
    global target, emote
    target = arg.replace("@!", "@")  # for some reason ordinary mention and author.mention differ - ordinary mention includes exclamation mark
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
                   value='Bot will count used on server reactions and emojis and will post statistics.', inline=False)
    post.add_field(name='!set_hi text1 text2 text3',
                   value='Bot will send a message when member joins the server.\ntext1 - text in quotation marks that will be placed before mentioning new member\ntext2 - text in quotation marks that will be placed between mention and your server name\ntext3 - text in quotation marks that will be placed after your server name',
                   inline=False)
    post.add_field(name='!set_bye text1 text2',
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
    print(date)
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
    print('Step 1')
    for channel in bot.get_all_channels():  # cycle of messages on server
        if channel.type.name == 'text':
            messages = await channel.history(limit=None, after=date).flatten()
            for message in messages:
                if message.reactions.__len__ is not None:  # reaction counting
                    for reaction in message.reactions:
                        for counter in reaction_counter:
                            print('Step 0.3')
                            if counter[0] == reaction.emoji:
                                counter[1] = counter[1] + reaction.count
                for emoji in reaction_counter:  # emoji counting in text
                    print('Step 0.5')
                    string = ':' + emoji[0].name + ':'
                    if string in message.content:
                        emoji[1] = emoji[1] + 1
    print('Step 2')
    reaction_counter.sort(key=emoji_sort)
    for emoji in reaction_counter:
        await ctx.send(f'{emoji[0]} - {emoji[1]}.')
        print('Step 0.7')
        if emoji[1] <= 10:
            await emoji[0].delete(reason='Использовалась меньше десяти раз.')
    print('Step 3')


if __name__ == "__main__":
    bot.run(botconfig.TOKEN)
