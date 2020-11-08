import discord
from discord import Intents
from discord.ext.commands import Bot, has_permissions
import botconfig

intents = Intents(members=True, guilds=True, messages=True, reactions=True)
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
async def emoji_date(ctx, arg):  # set the day of the month, when bot will start counting
    ec_date = arg
    await ctx.send(f'Подсчёт включён, установленная дата: {ec_date} число.')


'''
@bot.command()
async def emoji_counting(ctx, arg):
    if arg == 'on':
        # ON CODE
        list_of_messages = []
        #reactions = []
        for channel in bot.get_all_channels():
            if channel.type.name == 'text':
                messages = await channel.history(limit=None).flatten()
                list_of_messages.extend(messages)
        for message in list_of_messages:
            rec = ctx.author.fetch_message(771059276239077406)
            #if message.reactions >0:
            #reac = message
            print('logged on')

            #mes = message.author.fetch_message(message.id)
            #reactions = discord.utils.get(message.reactions)
        print(channel)
        print('logged on')
        await ctx.send(f'Подсчёт включён, {ctx.message.author.mention}.')
'''


@bot.command()
@has_permissions(administrator=True)
async def mes(ctx):
    reaction_counter = []
    for emoji in ctx.author.guild.emojis:  # list of custom emojis
        ctr = [emoji, 0]
        reaction_counter.append(ctr)
    for channel in bot.get_all_channels():  # cycle of messages on server
        if channel.type.name == 'text':
            messages = await channel.history(limit=None).flatten()
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
    for emoji in reaction_counter:
        await ctx.send(f'{emoji[0]} - {emoji[1]}.')


@bot.command()
@has_permissions(administrator=True)
async def reacts(ctx, arg, arg1):  # setting the target of reactions
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
