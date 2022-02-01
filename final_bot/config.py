import os

from dotenv import load_dotenv

load_dotenv()
TG_TOKEN = os.getenv("TG_TOKEN")

SECRET_KEY = os.getenv("SECRET_KEY")

ACCESS_KEY = os.getenv("ACCESS_KEY")
BUCKET = "kate-picture-bot"
