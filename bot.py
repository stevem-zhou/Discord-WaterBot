import hikari
import lightbulb
from tooken import tokin
from lightbulb.ext import tasks


bot = lightbulb.BotApp(
    token= tokin, 
    intents=hikari.Intents.ALL_UNPRIVILEGED | hikari.Intents.GUILD_PRESENCES | hikari.Intents.GUILD_MEMBERS,
    help_slash_command=True
    )


tasks.load(bot)

bot.load_extensions_from('./extensions')

bot.run(activity=hikari.Activity(name='MERRY CHRISTMAS - Chieri Itō', type=hikari.ActivityType.LISTENING))