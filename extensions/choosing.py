import lightbulb
import hikari
import random


lightbulb.BotApp.default_enabled_guilds = []
choosing_plugin = lightbulb.Plugin("Random Decider")

@choosing_plugin.command()
@lightbulb.add_checks(lightbulb.dm_only)
@lightbulb.option('different_options', 'Separate the options with a semicolon ";"')
@lightbulb.command('decide', 'Chopper will help decide between options')
@lightbulb.implements(lightbulb.SlashCommand)
async def decide(ctx: lightbulb.context):
    temp_list = ctx.options.different_options.split(';')
    chosen = random.choice(temp_list)
    spaced_options = ' '.join(temp_list)
    await ctx.respond(f'Between {spaced_options}... I have decided on {chosen}!')


@choosing_plugin.listener(lightbulb.CommandErrorEvent)
async def checks(event: lightbulb.CommandErrorEvent):
    await event.context.respond(event.exception)


def load(bot):
    bot.add_plugin(choosing_plugin)