#Get Youtube html
import urllib.request
#Find all youtube IDs
import re
#Download and convert YT video
import youtube_dl
#Get last song downloaded
import shutil
import glob
import os
import sys
#Telegram Bot
import telebot

API_TOKEN = "YOUR_TOKEN"
bot = telebot.TeleBot(API_TOKEN)
@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Benvenuto nel bot! \nInserisci il nome o l'url del video da scaricare:")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, 'Download del file .mp3 in corso...')
    originalmessage = message.text
    #Replace spaces with -
    inputelement = originalmessage.replace(" ", "-")

    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + inputelement)

    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    complete_link = "https://www.youtube.com/watch?v=" + video_ids[0]   #Get the complete YT link

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([complete_link]) #Download the video

    mp3_file = glob.glob("*.mp3")  #consider only files with .mp3 extension
    newest_file = max(mp3_file, key=os.path.getctime)  #get the last file
    file_title = os.path.splitext(newest_file)[0] #get the title of file
    audio = open(file_title + '.mp3', 'rb')
    bot.send_audio(message.chat.id, audio)
    
print("Bot Online!\nListening...")
bot.polling()






