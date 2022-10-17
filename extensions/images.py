import hikari
import lightbulb
from pathlib import Path
import random


photosend = lightbulb.Plugin('Images')
used_pics = set()
list_of_pics = list(Path('chopper_photos').iterdir())

def photo_album():
    global used_pics
    global list_of_pics
    chosen = random.choice(list_of_pics)
    used_pics.add(chosen)
    list_of_pics.remove(chosen)
    if len(list_of_pics) == 0:
        for pic in used_pics:
            list_of_pics.append(pic)
        used_pics.clear()
        print('out of unused pictures!')
    print(chosen)
    return chosen


@photosend.command()
@lightbulb.add_checks(lightbulb.dm_only)
@lightbulb.command('chopper', 'chopper photos to boost seratonin')
@lightbulb.implements(lightbulb.SlashCommand)
async def image(ctx:lightbulb.Context):
    f = photo_album()
    if ctx.author.id != None: #None will be replaced by a targeted user_id
        await ctx.respond('Not available to you 0.0')
    else:
        await ctx.respond(f)


@photosend.listener(lightbulb.CommandErrorEvent)
async def checks(event: lightbulb.CommandErrorEvent):
    await event.context.respond(event.exception)


def load(bot):
    bot.add_plugin(photosend)