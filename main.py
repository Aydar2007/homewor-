"""Описание:
Сделать ToDo List Bot (Список дел) с использованием библиотек aiogram и aioshedule
Пользователь:
Пользователь может добавлять список своих дел (title, time) и данные должны попасть
в базу данных
И также пользователь может удалять свои дела
Также бот должен отправлять список дел пользователя по времени aioshedule
которую он указал при создании задания
ДОП ЗАДАНИЕ:
Использовать inline кнопки
Загрузить код в GitHub c .gitig"""

from dotenv import load_dotenv
from aiogram.types import KeyboardButton,InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup
import os,sqlite3,time,requests,logging,aioschedule
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, executor
from states import Time,Title,IdMessage,Delete
from aiogram.dispatcher import FSMContext

load_dotenv('.env')
bot = Bot(os.environ.get('token'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = sqlite3.connect('database.db')
cursor = db.cursor()
cursor.execute("""CREATE TABLE  IF NOT EXISTS orders(
    id INT,
    id_list INT,
    title VARCHAR (500),
    time VARCHAR (100) 
);
""")
cursor.connection.commit()




inline_buttons1 = [
    InlineKeyboardButton('Добавить в список дел',callback_data='inline_creat'),
    InlineKeyboardButton('Удалить сообщение(укажите номер сообщения)',callback_data='inline_delate')
]
inline1 = InlineKeyboardMarkup().add(*inline_buttons1)


inline_buttons2 = [
    InlineKeyboardButton('Укажите №сообщения',callback_data='inline_idmes'),
]
inline2 = InlineKeyboardMarkup().add(*inline_buttons2)

inline_buttons3 = [
    InlineKeyboardButton('Добавить заголовок в список дел',callback_data='inline_list')
]
inline3 = InlineKeyboardMarkup().add(*inline_buttons3)


inline_buttons4 = [
    InlineKeyboardButton('Указать время ',callback_data='inline_times'),
]
inline4 = InlineKeyboardMarkup().add(*inline_buttons4)


@dp.callback_query_handler(lambda call: call)
async def all_inline(call):
    if call.data == 'inline_creat':
        await creats (call.message)
    elif call.data == 'inline_delete':
        await deletes(call.message,state=None)
    elif call.data == "inline_idmes":
        await idmessages (call.message,state=None)
    elif call.data == "inline_list":
        await titles (call.message,state=None)
    elif call.data == "inline_times":
        await timess (call.message,state=None)

@dp.message_handler(commands="start")
async def start (message:types.Message):
    cursor=db.cursor()
    cursor.execute(f"SELECT id FROM orders WHERE id = {message.from_user.id};")
    res = cursor.fetchall()
    if res == []:
        cursor.execute(f"""INSERT INTO orders VALUES (
            {message.from_user.id},
            '{0}',
            '{0}',
            '{0}'

        );""")
        cursor.connection.commit()
    await message.answer(f"Привет{message.from_user.full_name}",reply_markup=inline1)

@dp.message_handler(commands="creat")
async def creats (message:types.Message):
    await message.answer("перейдем к следуещему для создания",reply_markup=inline2)

@dp.message_handler(commands="idmessage", state=None)
async def idmessages(message:types.Message):
    await message.answer("Укажите id для сообщения(формат:1 или 2)",reply_markup=inline3)
    await IdMessage.set()
    
@dp.message_handler(state=IdMessage)
async def idmessages(message:types.Message,state:FSMContext):
    cursor = db.cursor()
    cursor.execute(f"UPDATE orders SET id_list = {message.text} WHERE id = {message.from_user.id};")
    cursor.connection.commit() 

@dp.message_handler(commands="title", state=None)
async def titles (message:types.Message):
    await message.answer("Укажите id для сообщения(формат:1 или 2)",reply_markup=inline4)
    await Title.set()
    
@dp.message_handler(state=Title)
async def titles(message:types.Message,state:FSMContext):
    cursor = db.cursor()
    cursor.execute(f"UPDATE orders SET title = {message.text} WHERE id = {message.from_user.id};")
    cursor.connection.commit() 

@dp.message_handler(commands="times", state=None)
async def timess (message:types.Message):
    await message.answer("Укажите id для сообщения(формат:1 или 2)",reply_markup=inline1)
    await Time.set()
    
@dp.message_handler(state=Time)
async def timess(message:types.Message,state:FSMContext):
    cursor = db.cursor()
    cursor.execute(f"UPDATE orders SET time = {message.text} WHERE id = {message.from_user.id};")
    cursor.connection.commit() 

@dp.message_handler(commands="delete", state=None)
async def deletes (message:types.Message):
    await message.answer("Какой номер сообщения удалить'без знака № ,просто цифра?'")
    await Delete.set()

@dp.message_handler(state=Delete)
async def deletes(message:types.Message,state:FSMContext):

    cursor = db.cursor()
    cursor.execute(f"DELETE title FROM orders WHERE id = {message.from_user.id},id_list = {message.text};")
    cursor.connection.commit() 
    cursor = db.cursor()
    cursor.execute(f"DELETE time FROM orders WHERE id = {message.from_user.id},id_list = {message.text};")
    cursor.connection.commit() 
    cursor = db.cursor()
    cursor.execute(f"DELETE id_list FROM orders WHERE id = {message.from_user.id},id_list = {message.text};")
    cursor.connection.commit()

executor.start_polling(dp)
