# bot.py
import os, datetime, json, asyncio

from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')
channel_id=943720617780334635

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

def get_schedule():
    week_num = datetime.date.today().isocalendar()[1]
    partners = pairs[week_num%len(pairs)]

    pretty_partners = ''

    for key in partners:
        pretty_partners += '{}:\t{}, {}\n'.format(key, partners[key][0], partners[key][1])

    return pretty_partners

# Sends schedule message out once a week (24 * 7)
@tasks.loop(hours=168)
async def send_weekly_schedule():
    await bot.get_channel(channel_id).send(get_schedule())

@send_weekly_schedule.before_loop
async def before_send_weekly_schedule():
    weekday_num = datetime.datetime.today().weekday()

    # Sunday is 6
    if(weekday_num != 0):
        # Calculate number of seconds till Sunday and sleep before sending
        seconds_till_sunday = (6-weekday_num)*24*60*60
        await asyncio.sleep(seconds_till_sunday)

@bot.command(name='partners', help='Tells you who you are paired with this week 👍')
async def send_partners_message(ctx):

    author = usernames[ctx.author.discriminator]
    week_num = datetime.date.today().isocalendar()[1]
    partners = pairs[week_num%len(pairs)][author]

    await ctx.send('{}\'s partners this week are {} and {}'.format(author, partners[0], partners[1]))

@bot.command(name='schedule', help='Full schedule for this week')
async def send_schedule_message(ctx):
    await ctx.send('Schedule for this week:\n{}'.format(get_schedule()))

@bot.command(name='loop', help='Starts loops for bot')
async def send_schedule_message(ctx):
    send_weekly_schedule.start()

bot.run(TOKEN)
