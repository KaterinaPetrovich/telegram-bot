import os

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from config import TG_TOKEN, admins
from helper import remove_dir, remove_gif
from keyboards import font_size_keyboard, fonts_keyboard
from picture_handler import add_text_to_picture, create_gif
from s3_connection import (download_all_gifs, download_users_gifs, upload_gif,
                           upload_picture, upload_private_gif)

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class PictureModif(StatesGroup):
    picture = State()
    text = State()
    font = State()
    font_size = State()


class Gif(StatesGroup):
    gif = State()


@dp.message_handler(commands=["start", "help"])
async def start(message: types.Message):
    """Responds to commands /start and /help. Send welcome message"""
    await message.answer(
        "Hello! I am PictureBot. \n"
        "I can add text to your picture and create gif. \n"
        "My commands: \n"
        "/addtext - adds text to picture \n"
        "/creategif - creates gif from your pictures \n"
        "/getallgifs - use it to see all "
        "gifs created by users \n"
        "/getmygifs  - use it to see only your gifs "
    )


@dp.message_handler(commands=["addtext"], state=None)
async def start_mode(message: types.Message):
    """Responds to command /addtext. Sends message with instructions"""
    await PictureModif.picture.set()
    await message.answer("Send photo")


@dp.message_handler(commands=["creategif"], state=None)
async def start_mode(message: types.Message):
    """Responds to command /creategif. Sends message with instructions"""
    await Gif.gif.set()
    await message.answer(
        "Send photos. After sending use command /getgif "
        "or /privategif for private gif"
    )


@dp.message_handler(content_types=["photo"], state=Gif.gif)
async def load_photo_for_gif(message: types.Message):
    """
    Gets photo for gif and saves it
    """
    file_id = message.photo[-1].file_id
    user_id = message.from_user.id

    await message.photo[-1].download(
        destination_file=f"{user_id}" f"gif/{file_id}.jpg"
    )


@dp.message_handler(commands=["getgif"], state=Gif.gif)
async def create_public_gif(message: types.Message, state: FSMContext):
    """
    Creates public gif and sends it to user. Removes dir with photos
    """
    user_id = message.from_user.id
    gif_path = create_gif(f"{user_id}gif/")
    upload_gif(user_id, gif_path)
    with open(gif_path, "rb") as gif:
        await bot.send_animation(message.from_user.id, gif)
    await state.finish()
    remove_dir(f"{user_id}gif/")


@dp.message_handler(commands=["privategif"], state=Gif.gif)
async def create_private_gif(message: types.Message, state: FSMContext):
    """
    Makes gif private and sends it to user. Removes dir with photos
    """
    user_id = message.from_user.id
    gif_path = create_gif(f"{user_id}gif/")
    upload_private_gif(user_id, gif_path)
    with open(gif_path, "rb") as gif:
        await bot.send_animation(message.from_user.id, gif)
    await state.finish()
    remove_dir(f"{user_id}gif/")


@dp.message_handler(commands=["getallgifs"])
async def get_gif(message: types.Message):
    """
    Responds to the command /getallgifs
    and sends to user all existing gifs. Sends appropriate message if
    there is no gifs
    """
    gifs = download_all_gifs()
    print(gifs)
    if gifs:
        for gif_name in gifs:
            with open(gif_name, "rb") as gif:
                await bot.send_animation(message.chat.id, gif)
        remove_gif()
    else:
        await message.answer("There are no gifs. \n" 
                             "Use /creategif to create one")


@dp.message_handler(commands=["getmygifs"])
async def get_gif(message: types.Message):
    """
    Responds to the command /getmygifs
    and sends to user his or her gifs. Sends appropriate message if
    user doesn't have any gifs
    """
    gifs = download_users_gifs(message.from_user.id)
    if gifs:
        for gif_name in gifs:
            print(gif_name)
            with open(gif_name, "rb") as gif:
                await bot.send_animation(message.chat.id, gif)
        remove_gif()
    else:
        await message.answer(
            "You don't have any gifs yet. \n" "Use /creategif to create one"
        )


@dp.message_handler(content_types=["photo"], state=PictureModif.picture)
async def load_photo(message: types.Message, state: FSMContext):
    """Gets photo and saves"""
    file_id = message.photo[-1].file_id
    await message.photo[-1].download(destination_file="photos/" 
                                                      f"{file_id}.jpg")
    async with state.proxy() as data:
        data["photo"] = file_id
    await PictureModif.next()
    await message.answer("Send text")


@dp.message_handler(state=PictureModif.font)
async def save_font(message: types.Message, state: FSMContext):
    """Gets font name and saves"""
    async with state.proxy() as data:
        data["font"] = message.text
        await message.answer("Please choose font size",
                             reply_markup=font_size_keyboard)
        await PictureModif.next()


@dp.message_handler(state=PictureModif.font_size)
async def apply_parameters_and_send_photo(message: types.Message,
                                          state: FSMContext):
    """
    Applies all parameters and sends image with added text
    """
    async with state.proxy() as data:
        text = data["text"]
        font = data["font"]
        font_size = int(message.text)
        photo_id = data["photo"]
        photo_path = "photos/" + photo_id + ".jpg"
        add_text_to_picture(text, photo_path, font, font_size)
    upload_picture(message.from_user.id, photo_path, photo_id)
    await bot.send_photo(
        message.chat.id,
        types.InputFile(photo_path),
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.finish()
    remove_dir("photos/")


@dp.message_handler(state=PictureModif.text)
async def add_text(message: types.Message, state: FSMContext):
    """gets text and saves it"""
    async with state.proxy() as data:
        data["text"] = message.text
        await message.answer("Please choose font", reply_markup=fonts_keyboard)
        await PictureModif.next()


executor.start_polling(dp, skip_updates=True)
