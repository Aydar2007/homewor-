from aiogram.types import KeyboardButton,InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup
inline_buttons1 = [
    InlineKeyboardButton('creat',callback_data='inline_creat'),
    InlineKeyboardButton('delete',callback_data='inline_delate')
]
inline1 = InlineKeyboardMarkup().add(*inline_buttons1)


inline_buttons2 = [
    InlineKeyboardButton('id_message',callback_data='inline_idmes'),
]
inline2 = InlineKeyboardMarkup().add(*inline_buttons2)

inline_buttons3 = [
    InlineKeyboardButton('title',callback_data='inline_list')
]
inline3 = InlineKeyboardMarkup().add(*inline_buttons3)


inline_buttons4 = [
    InlineKeyboardButton('times',callback_data='inline_times'),
]
inline4 = InlineKeyboardMarkup().add(*inline_buttons4)