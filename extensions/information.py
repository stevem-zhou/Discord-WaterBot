import lightbulb
import hikari
from tooken import stevem_id

lightbulb.BotApp.default_enabled_guilds = []
readme_plugin = lightbulb.Plugin('Read Me')
with open('info.txt') as info_file:
    line = info_file.read()


@readme_plugin.command()
@lightbulb.add_checks(lightbulb.dm_only)
@lightbulb.command('read_me', 'Info about bot')
@lightbulb.implements(lightbulb.SlashCommand)
async def special(ctx: lightbulb.context):
    global line
    if ctx.author.id != stevem_id: #None will be replaced by a targeted user_id
        await ctx.respond('Not available to you 0.0')
    else:
        await ctx.respond(f"```{line}```")


def load(bot):
    bot.add_plugin(readme_plugin)