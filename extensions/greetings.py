import hikari
import lightbulb
import random
import datetime
from tooken import stevem_id


greeting_plugin = lightbulb.Plugin('Greetings')
nicknames = ['Kit-Kat', 'Air Head', 'Jolly Rancher',
             'Jelly Bean', 'Tootsie Roll', 'Twix', 'Whopper',
              'Malteser', 'Almond Joy', 'Candy Corn', 'Skittles',
               'Starburst', 'Hersheys']
            

@greeting_plugin.listener(hikari.PresenceUpdateEvent)
async def starting_greet(event: hikari.PresenceUpdateEvent):
    if (event.user_id != stevem_id): #None will be replaced by a targeted user_id
        return
    time = datetime.datetime.now()
    greeting = f'Good morning {random.choice(nicknames)}!' if time.hour < 12 else \
                f'Good afternoon {random.choice(nicknames)}!' if 12 <= time.hour <= 18 else \
                f'Good evening {random.choice(nicknames)}!'
    dm_channel = await greeting_plugin.bot.rest.create_dm_channel(stevem_id) #None will be replaced by a targeted user_id
    if (event.old_presence and event.old_presence.visible_status == event.presence.visible_status):
        return
    if not event.old_presence:
        await dm_channel.send(greeting)
    elif event.old_presence.visible_status in ('OFFLINE', None) \
            and event.presence.visible_status in ('ONLINE', 'DO_NOT_DISTURB', 'IDLE'):
        await dm_channel.send(greeting)


def load(bot):
    bot.add_plugin(greeting_plugin)