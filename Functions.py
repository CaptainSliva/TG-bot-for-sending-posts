from pyrogram import Client
import random
import os
from pathlib import Path


def pars_file(m):
    with open('config.txt', 'r', encoding='utf-8') as f:
        file = f.readlines()
        for i in file:
            if m in i:
                return i.split('"')[1]
            

api_id = pars_file('api_id')
api_hash = pars_file('api_hash')
short_name = pars_file('short_name')
phone_number = pars_file('phone_number')
botmname = pars_file('botname')
bot_id = None
app = Client(short_name, api_id=api_id, api_hash=api_hash, phone_number=phone_number)
with app:
    for dialog in app.get_dialogs():
                if dialog.chat.username == botmname:
                    my_last_message = dialog.top_message.id
                    print(dialog.top_message.id)
                    bot_id = dialog.chat.id
print(bot_id)

async def avaliable_channels():
    app = Client(short_name, api_id=api_id, api_hash=api_hash, phone_number=phone_number)

    async with app:
        chats = '\n'.join([dialog.chat.title async for dialog in app.get_dialogs() if dialog.chat.title != None])
    return chats



async def random_message():
    app = Client(short_name, api_id=api_id, api_hash=api_hash, phone_number=phone_number)
    c = await avaliable_channels()
    c = c.split('\n')
    n = random.randint(0, len(c)-1)
    c = c[n]
    print(n)
    async with app:
        async for dialog in app.get_dialogs():
            if str(dialog.chat.title) == c:
                print(dialog.chat.title)
                await app.copy_message(bot_id, dialog.chat.id, dialog.top_message.id)
                try:
                    await app.download_media(dialog.top_message.photo.file_id)
                    print('photoooooooo')
                except: 
                    print(dialog.chat.title)
                    

                break





async def download_photo():
    app = Client(short_name, api_id=api_id, api_hash=api_hash, phone_number=phone_number)
    async with app:
        async for dialog in app.get_dialogs():
            if dialog.chat.username == botmname:
                await app.download_media(dialog.top_message.photo.file_id)
    return sorted(Path(f'{os.getcwd()}/downloads').iterdir(), key=os.path.getmtime)[-1]



async def text():
    app = Client(short_name, api_id=api_id, api_hash=api_hash, phone_number=phone_number)
    async with app:
        async for dialog in app.get_dialogs():
            if dialog.chat.username == botmname:

                if dialog.top_message.text != None:
                    return [0, dialog.top_message.text]
                
                if dialog.top_message.photo.file_id != None:
                    photo = list()
                    await app.download_media(dialog.top_message.photo.file_id)
                    photo.append(sorted(Path(f'{os.getcwd()}/downloads').iterdir(), key=os.path.getmtime)[-1])
                    if dialog.top_message.caption != None:
                        photo.append(dialog.top_message.caption)
                return [1, photo]
            

# print(asyncio.run(random_message()))
      

