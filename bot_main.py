#Get Youtube html
import urllib.request
#Find all youtube IDs
import re
import requests
#Download and convert YT video
import youtube_dl
#Get last song downloaded / delete last song/video
import shutil
import glob
import os
import sys
#Telegram Bot
import telebot

#Telegram bot start
API_TOKEN = ""
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Benvenuto nel bot! Controlla /help per tutti i comandi a tua disposizione.\nInserisci il nome o l'url del video da scaricare:")
#Help commands

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "Benvenuto nel bot! \nInserisci il nome o l'url del video da scaricare:")

#Download video/audio
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, 'Download del file .mp3 in corso...')
    originalmessage = message.text

    #Replace spaces with -
    inputelement = originalmessage.replace(" ", "-")

    #Print loading
    bot.reply_to(message, 'Ricerca del video... (10%)')

    #Get html page of youtube
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + inputelement)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    #Find video link
    complete_link = "https://www.youtube.com/watch?v=" + video_ids[0]   #Get the complete YT link
    #Find video name
    r_completelink = requests.get(complete_link)
    r_html_text = r_completelink.text
    video_name = re.findall("title=\"[^\"]*\"", r_html_text)
    video_name_splitted = [i.lower().replace('title="', '').split() for i in video_name]

    print(video_name_splitted)
    bot.reply_to(message, 'Download del video: ')
    bot.reply_to(message, video_name[2])
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
    bot.reply_to(message, 'Conversione e upload del video... (70%)')

    mp3_file = glob.glob("*.mp3")  #consider only files with .mp3 extension
    newest_file = max(mp3_file, key=os.path.getctime)  #get the last file
    file_title = os.path.splitext(newest_file)[0] #get the title of file
    audio = open(file_title + '.mp3', 'rb')
    bot.send_audio(message.chat.id, audio)

    #Delete last song / video downloaded
    audio.close()
    os.remove(file_title + '.mp3')

print("Bot Online!\nListening...")
bot.polling()






