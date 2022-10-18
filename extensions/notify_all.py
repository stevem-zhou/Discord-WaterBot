import hikari
import lightbulb

lightbulb.BotApp.default_enabled_guilds = []
notify_plugin = lightbulb.Plugin("Notify")

@notify_plugin.listener(hikari.StartedEvent)
async def notify(event: hikari.StartedEvent):
    cache = await notify_plugin.bot.rest.fetch_my_guilds()
    # print(type(cache[0]))
    
    




def load(bot):
    bot.add_plugin(notify_plugin)