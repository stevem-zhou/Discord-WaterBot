import hikari
import lightbulb
import gspread


lightbulb.BotApp.default_enabled_guilds = []
notify_plugin = lightbulb.Plugin("Notify")

@notify_plugin.listener(hikari.StartedEvent)
async def notify(event: hikari.StartedEvent):
    cache = await notify_plugin.bot.rest.fetch_my_guilds()
    members = notify_plugin.bot.rest.fetch_members(cache[1])
    async for member in members:
        await upload(str(member), str(member.user.id))
        await download()
    
async def upload(username, id):
    gc = gspread.service_account(filename='creds.json')
    sh = gc.open('discordIDs').sheet1
    sh.append_row([username, id])
    return


async def download():
    gc = gspread.service_account(filename='creds.json')
    sh = gc.open('discordIDs').sheet1
    return sh.get_all_records()

def load(bot):
    bot.add_plugin(notify_plugin)