import glob
import time

from helper import fonts
from PIL import Image, ImageDraw, ImageFont


def add_text_to_picture(text, pic_path, font_name, fontsize):
    """Adds text to the picture and saves it"""
    img = Image.open(pic_path)
    w_pic, h_pic = img.size
    draw = ImageDraw.Draw(img)
    font_path = fonts[font_name]
    font = ImageFont.truetype(font_path, fontsize, encoding="UTF-8")
    w_font, _ = font.getsize(text)
    draw.text(
        (w_pic / 2 - w_font / 2, h_pic * 6 / 8),
        text,
        fill="white",
        stroke_fill="black",
        stroke_width=4,
        font=font,
    )
    img.save(pic_path)


def add_watermark(pic_path):
    add_text_to_picture("PictureBot", pic_path, "Vivaldi", 30)


def create_gif(path_to_pictures):
    """Creates gif from the pictures"""
    images = []
    for name in glob.glob(path_to_pictures + "*.jpg"):
        add_watermark(name)
        img = Image.open(name)
        images.append(img)

    timestr = time.strftime("%Y%m%d-%H%M%S")
    gif_path = f"{path_to_pictures}gif{timestr}.gif"
    images[0].save(
        gif_path,
        save_all=True,
        append_images=images[1:],
        optimize=False,
        duration=100,
        loop=0,
    )
    return gif_path
