import os

from helper import remove_gif
from picture_handler import add_text_to_picture, create_gif
from PIL import Image, ImageChops
from s3_connection import download_all_gifs, download_users_gifs


def test_add_text_to_picture():
    """
    Test function compares pictures before adding text and after
    """
    add_text_to_picture("text", "test_photo/2.jpg", "Times new roman", 100)
    img1 = Image.open("test_photo/1.jpg")
    img2 = Image.open("test_photo/2.jpg")
    result = ImageChops.difference(img1, img2)
    assert result


def test_download_users_gifs():
    """
    Test function checks downloading users gif
    """
    gifs = download_users_gifs(897250863)
    assert gifs
    remove_gif()


def test_download_non_existing_users_gifs():
    """
    Test function checks downloading users gif
    """
    gifs = download_users_gifs(897250833)
    assert not gifs


def test_download_all_gifs():
    """
    Test function checks downloading all gif
    """
    gifs = download_all_gifs()
    assert gifs
    remove_gif()


def test_create_gif():
    gif_path = create_gif("test_photo/gif/")
    assert ".gif" in gif_path
    os.remove(gif_path)
