import hikari
import lightbulb
import datetime


log_plugin = lightbulb.Plugin('logging')


@log_plugin.listener(hikari.DMMessageCreateEvent)
async def log_chat(event: hikari.DMMessageCreateEvent):
    with open('log.txt', mode='a') as file:
        lines = event.content
        file.write(str(event.author) + ': ' + lines + ' ' + str(datetime.datetime.now()) + '\n')


def load(bot):
    bot.add_plugin(log_plugin)