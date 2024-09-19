from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


Channels = KeyboardButton('Доступные каналы')
Set_interval = KeyboardButton('Интервал')
Posting = KeyboardButton('Пост')
Start = KeyboardButton('Старт')
Viev = KeyboardButton('Посмотреть пост')
Main = KeyboardButton('Главное меню')

Stop = KeyboardButton('Остановка')



MainMenu = ReplyKeyboardMarkup(resize_keyboard=True).row(Channels, Set_interval).row(Posting, Start)
StopSpam = ReplyKeyboardMarkup(resize_keyboard=True).add(Stop)
VievPost = ReplyKeyboardMarkup(resize_keyboard=True).add(Viev)
MainPost = ReplyKeyboardMarkup(resize_keyboard=True).add(Main)


Replace_photo = InlineKeyboardButton(text='Изменить фото', callback_data='Изменить фото/foto')
Replace_text = InlineKeyboardButton(text='Изменить текст', callback_data='Изменить текст/foto')
Delete_photo = InlineKeyboardButton(text='Удалить фото', callback_data='Удалить фото/foto')


InlineMenu = InlineKeyboardMarkup().add(Replace_photo).add(Replace_text).add(Delete_photo)
