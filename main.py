import logging as log
from aiogram import Bot, Dispatcher, executor, types
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import Buttons as btn
import Functions as pg


def normal(s):
    return s.split('/')[0]

def pars_file(m):
    with open('config.txt', 'r', encoding='utf-8') as f:
        file = f.readlines()
        for i in file:
            if m in i:
                return i.split('"')[1]
            

TOKEN = pars_file('token')


#Создаем telegram бота
log.basicConfig(level = log.INFO) # Включаем логирование чтобы не пропустить важные сообщения
bot = Bot(token = TOKEN) # Создаем обьект бота
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage) # Диспетчер


class UserState(StatesGroup):
    new_photo = State()
    new_text = State()
    del_photo = State()
    result = State()


class Message():
    photo = None
    text = None
    what_to_do = None


@dp.message_handler(commands=['start'])
async def get_chats(message: types.Message):
    await message.answer(f'Здравствуйте! {message.from_user.full_name}', reply_markup=btn.MainMenu)
        


@dp.message_handler()
async def get_chats(message: types.Message):
    
    if message.text == 'Доступные каналы':
        # функция пирога       *
        channels = await pg.avaliable_channels()
        # print(channels)
        await bot.send_message(message.from_user.id, channels)

        
        
    # if message.text == 'Интервал':
        #функция для задания интервала сообщений      *

    if message.text == 'Пост':
        Message.text = Message.photo = None
        # рандомный пост через пирог
        await pg.random_message()

        bot_message = await pg.text()
        if bot_message[0] == 0:
            Message.text = bot_message[1]
        
        if bot_message[0] == 1:
            if len(bot_message) == 3:
                Message.text = bot_message[-1][-1]
            Message.photo = bot_message[1]


        await message.answer('↑Ваш пост↑', reply_markup=btn.InlineMenu)
        




    @dp.callback_query_handler(text =  'Изменить фото/foto')
    async def callbacks_num(callback: types.CallbackQuery):
        await callback.answer()
        await UserState.new_photo.set()
        await bot.send_message(message.from_user.id, 'Прикрепи фотографию именно как фото, а не файл')

        @dp.message_handler(state=UserState.new_photo, content_types = ['photo'])
        async def get_username(message: types.Message, state: FSMContext):
            photo = await pg.download_photo()
            await state.update_data(new_photo=photo)
            await bot.send_message(message.from_user.id, 'Фото загружено', reply_markup=btn.VievPost)
            await UserState.result.set()

        # @dp.message_handler(state=UserState.result)
        # async def get_username(message: types.Message, state: FSMContext):
        #     data = await state.get_data()
        #     photo = open(data['new_photo'], 'rb')
        #     await bot.send_photo(message.from_user.id, photo, caption=Message.text, reply_markup=btn.MainPost)
        #     await UserState.next()




    @dp.callback_query_handler(text =  'Изменить текст/foto')
    async def callbacks_num(callback: types.CallbackQuery):
        await callback.answer()
        await UserState.new_text.set()
        await bot.send_message(message.from_user.id, 'Введите текст')

        @dp.message_handler(state=UserState.new_text, content_types = ['text'])
        async def get_username(message: types.Message, state: FSMContext):
            Message.text = message.text
            await bot.send_message(message.from_user.id, 'Текст загружен', reply_markup=btn.VievPost)
            await UserState.result.set()

        # @dp.message_handler(state=UserState.result)
        # async def get_username(message: types.Message, state: FSMContext):
        #     try:
        #         photo = open(Message.photo, 'rb')
        #         await bot.send_photo(message.from_user.id, photo, caption=Message.text, reply_markup=btn.MainPost)
        #     except:
        #         await bot.send_message(message.from_user.id, Message.text, reply_markup=btn.MainPost)
        #     await UserState.next()




    @dp.callback_query_handler(text =  'Удалить фото/foto')
    async def callbacks_num(callback: types.CallbackQuery):
        await callback.answer()
        await UserState.result.set()
        await bot.send_message(message.from_user.id, 'Фото удалено', reply_markup=btn.VievPost)

    @dp.message_handler(state=UserState.result)
    async def get_username(message: types.Message, state: FSMContext):
        if Message.what_to_do == 'new_photo':
            data = await state.get_data()
            photo = open(data['new_photo'], 'rb')
            await bot.send_photo(message.from_user.id, photo, caption=Message.text, reply_markup=btn.MainPost)
            await UserState.next()
        if Message.what_to_do == 'new_text':
            try:
                photo = open(Message.photo, 'rb')
                await bot.send_photo(message.from_user.id, photo, caption=Message.text, reply_markup=btn.MainPost)
            except:
                await bot.send_message(message.from_user.id, Message.text, reply_markup=btn.MainPost)
            await UserState.next()
        if Message.what_to_do == 'del_photo':
            await bot.send_message(message.from_user.id, Message.text, reply_markup=btn.MainPost)
            # await bot.send_message(message.from_user.id, 'YOU JUST POSTED CRINGE!!', reply_markup=btn.MainPost)
            await UserState.next()










    if message.text == 'Главное меню':
        await bot.send_message(message.from_user.id, 'В меню', reply_markup=btn.MainMenu)
    # if message.text == 'Старт':
        # for i in id_channels:
            # пирогом работаю копируя пост в остальные каналы

    # if message.text == 'Остановка':
        # это и выше будет в цикле и будет проверка переменой спама






executor.start_polling(dp, skip_updates=False)