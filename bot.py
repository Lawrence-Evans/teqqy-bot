# bot.py
import os
import random
import discord
import feedparser

from dotenv import load_dotenv
from discord.ext import commands, tasks

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

WowHeadFeed = feedparser.parse("https://www.wowhead.com/news&rss")
previousEntry = WowHeadFeed.entries[0]

#@tasks.loop(seconds=60.0)
#async def RssUpdate():
#    WowHeadFeed = feedparser.parse("https://www.wowhead.com/news&rss")
#    if(WowHeadFeed.entries[0].id == previousEntry.id):
#        response = WowHeadFeed.entries[0].link
 #       print(f'Link: ', WowHeadFeed.entries[0].link)
 #       previousEntry = WowHeadFeed.entries[0]


# CLI Messaging
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n\n - {members}')

    previousEntry = WowHeadFeed.entries[0]
    print(f'Displaying Posts uploaded after: ', previousEntry.id)



# Discord Channel Responses
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

@bot.command(name='getLatest', help='Shows latest article from Wowhead RSS Feed.')
async def get_latest_article(ctx):
    WowHeadFeed = feedparser.parse("https://www.wowhead.com/news&rss")
    response = WowHeadFeed.entries[0].link
    await ctx.send(response)


@bot.command(name='99', help='Responds with a random quote from Brooklyn 9-9.')
async def nine_nine(ctx):   
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        'Love, it sustains you. It’s like oatmeal.',
        'I’m fine at parties, I just stand in the middle of the room and don’t say anything.',
        'I am way too sleep-deprived to deal with your negativity right now.',
        'I’m gonna go cry in the bathroom, peace out homies',
        'I asked them if they wanted to embarrass you, and they instantly said yes.',
        'OK, no hard feelings, but I hate you. Not joking. Bye.',
        'Sarge, with all due respect, I am gonna completely ignore everything you just said.',
        'The English language can not fully capture the depth and complexity of my thoughts, so I’m incorporating emojis into my speech to better express myself. Winky face.',
        'If I die, turn my tweets into a book.',
        'Great, I’d like your $8-est bottle of wine, please.',
        'Captain Wuntch. Good to see you. But if you’re here, who’s guarding Hades?',
        'I’m playing Kwazy Cupcakes, I’m hydrated as hell, and I’m listening to Sheryl Crow. I’ve got my own party going on.',
        'Captain, turn your greatest weakness into your greatest strength. Like Paris Hilton RE: her sex tape.',
        'Jake, piece of advice: just give up. It’s the Boyle way. It’s why our family crest is a white flag.',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)
    
@bot.command(name='roll_dice', help='Simulates a Dice Roll.')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(','.join(dice))

# Assume all empty parentheses need ctx for discord along with async and await. Needs checking.
# Define the grid
class grid():
    rowOne = {
            1: 1,
            2: 2,
            3: 3
        }
    rowTwo = {
            4: 4,
            5: 5,
            6: 6
        }
    rowThree = {
            7: 7,
            8: 8,
            9: 9
        }

# Create grid
grid = Grid()        

@bot.command(name='O+Xs', help='Starts a game of noughts and crosses')
async def playerturn(ctx):
# Respond with starting grid
response = grid.rowOne.values()
await ctx.send(response)
response = grid.rowTwo.values()
await ctx.send(response)
response = grid.rowThree.values()
await ctx.send(response)

# Player taking a turn by choosing grid number and O or X
# a = int(input('Grid number'))
# b = str(input('O or X'))
# # Changing the grid
# if a in range(1, 4):
#     grid.rowOne.update({a: b})
# elif a in range(4, 7):
#     grid.rowTwo.update({a: b})
# elif a in range(7, 10):
#     grid.rowThree.update({a: b})
# # Grid updated with player move
# print(f'Grid number {a} is now {b} ')
# print(grid.rowOne.values())
# print(grid.rowTwo.values())
# print(grid.rowThree.values())
# # Text players turn
# playerturn()

# # Calling first turn
# playerturn()

# Role Restricted Actions
@bot.command(name='create-channel')
@commands.has_role('admin')
async def create_channel(ctx, channel_name='python'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)



# error handling
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

#RssUpdate.start()
bot.run(TOKEN)