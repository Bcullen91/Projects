from telethon import TelegramClient, sync
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
import xlsxwriter


# api_hash from https://my.telegram.org, under API Development.
api_id = 0 # ENTER UNIQUE API HERE
api_hash = '' # ENTER UNIQUE API HASH HERE
phone_number = '' # ENTER PHONE NUMBER HERE
chat_name = '' # ENTER YOUR UNIQUE CHAT ROOM NAME HERE
client = TelegramClient('testing', api_id, api_hash).start()
allUsers = []
workbook = xlsxwriter.Workbook('MoC_AllUsers.xlsx')
worksheet = workbook.add_worksheet('AllUsers')
row = 0
column = 0
name = ''
phone_num = []


async def get_all_users():
    me = await client.get_me()
    async for chats in client.iter_dialogs():
        if chats.name == chat_name:
            MoC = chats
    async for users in client.iter_participants('Miles of Credit'):
        fullName = str(users.first_name) + " " + str(users.last_name)
        if users.first_name == None:
            fullName = str(users.last_name)
        if users.last_name == None:
            if users.first_name == None:
                fullName = str(users.username)
            else:
                fullName = str(users.first_name)
        allUsers.append(fullName)


worksheet.write(row, column, 'Users')
row += 1

with client:
    client.loop.run_until_complete(get_all_users())

for user in allUsers:
    worksheet.write(row, column, user)
    row += 1



print(len(allUsers))

workbook.close()