import time

import yadisk

y = yadisk.YaDisk(token="AQAAAAA-YaklAAejtjQEy7i_2E1FmaaTUHyjT2M")
# y.mkdir("test")
# y.upload("homer.gif", "test/homer.gif")


def save_picture(user, picture):
    pass


# print(y.check_token())


def save_gif(user_id, gif):
    timestr = time.strftime("%Y%m%d-%H%M%S")

    if not y.is_dir("PictureBot/"):
        y.mkdir("PictureBot/")
        y
    y.upload(gif, "PictureBot/GIF/" f"{user_id}{timestr}.gif")
    print("mau")

    # y.mkdir("PictureBot/GIF/")
    print("maumau")


save_gif("asdf", "homer.gif")
