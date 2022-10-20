import gspread

gc = gspread.service_account(filename='creds.json')
sh = gc.open('discordIDs').sheet1

print(sh.get_all_records())