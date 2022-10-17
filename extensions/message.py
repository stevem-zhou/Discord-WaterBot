import lightbulb
import hikari
import random


lightbulb.BotApp.default_enabled_guilds = []
message_plugin = lightbulb.Plugin("Daily Message")
messages = ['"Success is not final; failure is not fatal: It is the courage to continue that counts." — Winston S. Churchill',
             '"It is better to fail in originality than to succeed in imitation." — Herman Melville',
             '"The road to success and the road to failure are almost exactly the same." — Colin R. Davis',
             '“Success usually comes to those who are too busy looking for it.” — Henry David Thoreau',
             '“Develop success from failures. Discouragement and failure are two of the surest stepping stones to success.” —Dale Carnegie',
             '“Do not let yesterday take up too much of today.” — Will Rogers',
             '“If you are working on something that you really care about, you do not have to be pushed. The vision pulls you.” — Steve Jobs',
             '“I am a greater believer in luck, and I find the harder I work the more I have of it.” — Thomas Jefferson',
             '“Opportunity is missed by most people because it is dressed in overalls and looks like work.” — Thomas Edison']

used_messages = set()


@message_plugin.command()
@lightbulb.add_checks(lightbulb.dm_only)
@lightbulb.add_cooldown(86400, 1, lightbulb.UserBucket)
@lightbulb.command('motd', 'a message of the day from Chopper')
@lightbulb.implements(lightbulb.SlashCommand)
async def magic(ctx: lightbulb.Context):
    global messages
    global used_messages
    chosen = random.choice(messages)
    used_messages.add(chosen)
    messages.remove(chosen)
    if len(messages) == 0:
        for i in used_messages:
            messages.append(i)
        used_messages.clear()
    if ctx.author.id != None: #None will be replaced by a targeted user_id
        await ctx.respond('Not available to you 0.0')
    else:
        await ctx.respond(chosen)


@message_plugin.listener(lightbulb.CommandErrorEvent)
async def checks(event: lightbulb.CommandErrorEvent):
    await event.context.respond(event.exception)


def load(bot):
    bot.add_plugin(message_plugin)