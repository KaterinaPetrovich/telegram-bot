from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

fonts_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ["Times new roman", "Vivaldi"]
fonts_keyboard.add(*buttons)

font_size_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ["30", "50", "70", "100", "200"]
font_size_keyboard.add(*buttons)
