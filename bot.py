# bot.py
import os
import datetime
import json

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

pairs = [
    {
        "Sean": ["Kevin", "Steven"],
        "Jimmy": ["Steven", "Kevin"],
        "Kevin": ["Sean", "Jimmy"],
        "Steven": ["Jimmy", "Sean"]
    },
    {
        "Sean": ["Jimmy", "Steven"],
        "Jimmy": ["Sean", "Kevin"],
        "Kevin": ["Steven", "Jimmy"],
        "Steven": ["Kevin", "Sean"]
    },
    {
        "Sean": ["Jimmy", "Kevin"],
        "Jimmy": ["Sean", "Steven"],
        "Kevin": ["Steven", "Sean"],
        "Steven": ["Kevin", "Jimmy"]
    }
]

usernames = {
    "6971": "Jimmy",
    "8829": "Sean",
    "2803": "Steven",
    "8384": "Kevin"
}

@bot.command(name='partners', help='Tells you who you are paired with this week 👍')
async def get_pairs(ctx):

    author = usernames[ctx.author.discriminator]
    week_num = datetime.date.today().isocalendar()[1]
    partners = pairs[week_num%len(pairs)][author]

    await ctx.send('{}\'s partners this week are {} and {}'.format(author, partners[0], partners[1]))

@bot.command(name='schedule', help='Full schedule for this week')
async def get_schedule(ctx):

    week_num = datetime.date.today().isocalendar()[1]
    partners = pairs[week_num%len(pairs)]

    pretty_partners = ''

    for key in partners:
        pretty_partners += '{}:\t{}, {}\n'.format(key, partners[key][0], partners[key][1])


    await ctx.send('Schedule for this week:\n{}'.format(pretty_partners))

bot.run(TOKEN)
