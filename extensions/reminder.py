import hikari
import lightbulb
from datetime import datetime, timedelta
from lightbulb.ext import tasks
import asyncio
from pathlib import Path
import random
from tooken import stevem_id


lightbulb.BotApp.default_enabled_guilds = []
reminder_plugin = lightbulb.Plugin('Reminder')
toggle_alert = True


def water_photo_album():
    p = Path('water_photos')
    return random.choice(list(p.iterdir()))


@reminder_plugin.command()
@lightbulb.add_checks(lightbulb.dm_only)
@lightbulb.command('toggle', 'toggle on/off stay hydrated alert')
@lightbulb.implements(lightbulb.SlashCommand)
async def toggle(ctx: lightbulb.Context):
    global toggle_alert
    if ctx.author.id != stevem_id: #None will be replaced by a targeted user_id
        return
    if toggle_alert:
        toggle_alert = False
        await ctx.respond('Thirst alert turned off!')
    else:
        toggle_alert = True
        await ctx.respond('Thirst alert turned on!')


@tasks.task(h=1, auto_start=True)
async def reminder():
    starting_time = datetime.now()
    global toggle_alert
    if toggle_alert:
        reminding_time = starting_time + timedelta(hours=1)
        wait_time = (reminding_time - starting_time).total_seconds()
        await asyncio.sleep(2)
        dm_chat = await reminder_plugin.bot.rest.create_dm_channel(stevem_id) #None will be replaced by a targeted user_id
        await dm_chat.send("DON'T FORGET TO DRINK WATER!", attachment=water_photo_album())
        await asyncio.sleep(wait_time)


def load(bot):
    bot.add_plugin(reminder_plugin)