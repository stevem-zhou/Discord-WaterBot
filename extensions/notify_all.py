import hikari
import lightbulb

lightbulb.BotApp.default_enabled_guilds = []
notify_plugin = lightbulb.Plugin("Notify")

@notify_plugin.listener(hikari.StartedEvent)
async def notify(event: hikari.StartedEvent):
    cache = await notify_plugin.bot.rest.fetch_my_guilds()
    members = notify_plugin.bot.rest.fetch_members(cache[1])
    async for i in members:
        print(i.user.id)
    
    
    




def load(bot):
    bot.add_plugin(notify_plugin)