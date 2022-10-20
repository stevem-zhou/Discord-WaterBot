import hikari
import lightbulb
import gspread
import miru


lightbulb.BotApp.default_enabled_guilds = []
notify_plugin = lightbulb.Plugin("Notify")


@notify_plugin.listener(hikari.StartedEvent)
async def notify(event: hikari.StartedEvent):
    member_iterators = await grab_servers()
    member_list = await grab_members(member_iterators)
    data_stored = await download()
    available_ids = await upload(member_list, data_stored)
    # sh.find('id').row gives row number
    # sh.find('id').col gives col number
    dm_chat = await notify_plugin.bot.rest.create_dm_channel(available_ids[0])
    await notify_plugin.bot.rest.add_reaction(dm_chat.id, 1032577215919038555, ":clown:")


    


async def upload(member_list, stored_data):
    gc = gspread.service_account(filename='creds.json')
    sh = gc.open('discordIDs').sheet1
    available_members = list()
    
    for member in member_list:
        if (member.user.id not in stored_data) and (member.user.id not in available_members):
            sh.append_row([str(member.user), str(member.user.id)])
            available_members.append(member.user.id)
        
    return available_members


async def download():
    gc = gspread.service_account(filename='creds.json')
    sh = gc.open('discordIDs').sheet1
    data = sh.get_all_records()
    data_list = list()

    for dict in data:
        data_list.append(dict['DiscordID'])
    
    return data_list


async def grab_members(member_iters):
    member_list = list()

    for i in range(len(member_iters)):
        async for member in member_iters[i]:
            member_list.append(member)

    return member_list
            

async def grab_servers():
    cache = await notify_plugin.bot.rest.fetch_my_guilds()
    member_iters = list()

    for server in cache:
        member_iters.append(notify_plugin.bot.rest.fetch_members(server))
    
    return member_iters


def load(bot):
    bot.add_plugin(notify_plugin)