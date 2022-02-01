import glob
import os


def remove_dir(dir_path):
    files = os.listdir(dir_path)
    for file in files:
        os.remove(f"{dir_path}{file}")
    os.rmdir(dir_path)


def remove_gif():
    for file in glob.glob(os.getcwd() + "/" + "*.gif"):
        os.remove(file)


fonts = {
    "Times new roman": "Fonts/times.ttf",
    "Freestyle": "Fonts/FREESCPT.ttf",
    "Vivaldi": "Fonts/Vivaldi script.ttf",
}
