import hikari
import lightbulb
import gspread


lightbulb.BotApp.default_enabled_guilds = []
notify_plugin = lightbulb.Plugin("Notify")


@notify_plugin.listener(hikari.StartedEvent)
async def notify(event: hikari.StartedEvent):
    member_iterators = await grab_servers()
    member_list = await grab_members(member_iterators)
    data_stored = await download()
    available_ids = await upload(member_list, data_stored)
    await msg_all(available_ids)


async def update_toggle(toggle: bool, id:str):
    gc = gspread.service_account(filename='creds.json')
    sh = gc.open('discordIDs').sheet1
    sh.update_cell(sh.find(id).row, sh.find(id).col + 1, toggle)
    

async def msg_all(all_ids: list):
    for id in all_ids:
        dm_chat = await notify_plugin.bot.rest.create_dm_channel(id)
        await dm_chat.send("Would you like to be reminded to drink water?", component=await build_btns())
        alert_toggle = await check_reaction(dm_chat)
        await update_toggle(alert_toggle, str(id))


async def check_reaction(chat_channel):
    try:
        button_clicked = await notify_plugin.bot.wait_for(hikari.InteractionCreateEvent, 30)
        if not isinstance(button_clicked.interaction, hikari.ComponentInteraction):
            return
        if button_clicked.interaction.custom_id == 'yes':
            await button_clicked.interaction.create_initial_response(
                hikari.ResponseType.MESSAGE_CREATE,
                "You have decided to turn on water alerts!",
                flags=hikari.MessageFlag.EPHEMERAL
            )
            return True
        elif button_clicked.interaction.custom_id == 'no':
            await button_clicked.interaction.create_initial_response(
                    hikari.ResponseType.MESSAGE_CREATE,
                    "You have decided to turn off water alerts!",
                    flags=hikari.MessageFlag.EPHEMERAL
                )
            return False
    except:
        await chat_channel.send("Your time to answer is up. If you would like to receive water alerts, use command: /toggle")
        pass


async def build_btns():
    button_row = notify_plugin.bot.rest.build_action_row()
    yes_button = button_row.add_button(hikari.ButtonStyle.PRIMARY, 'yes')
    yes_button.set_label('YES')
    yes_button.add_to_container()
    no_button = button_row.add_button(hikari.ButtonStyle.DANGER, 'no')
    no_button.set_label('NO')
    no_button.add_to_container()

    return button_row
    

async def upload(member_list, stored_data):
    gc = gspread.service_account(filename='creds.json')
    sh = gc.open('discordIDs').sheet1
    available_members = list()
    
    for member in member_list:
        if (member.user.id not in stored_data) and (member.user.id not in available_members) and (member.user.is_bot == False):
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