# Telegram PictureBot
Telegram bot, that can:  
receive from user picture and text -> return picture with text on it   
receive pictures -> return gif
# How to run it?
## Using Docker
1. Create .env file with environment variables TG_TOKEN, SECRET_KEY, ACCESS_KEY  
TG_TOKEN - telegram API token   
SECRET_KEY - secrem key from AWS S3 servis  
ACCESS_KEY - access key from AWS S3 servis  
2. Type "docker-compose up" in the command line
## Using virtualenv
1. Create virtualenv and activate it   
2. Set up dependencies from requirements.txt  
3. Create .env file as shown above   
4. Type "python bot.py" in the command line  
