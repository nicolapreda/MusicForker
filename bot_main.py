#Get Youtube html
import urllib.request
from urllib.request import Request, urlopen
import lxml.html as LH

#Find all youtube IDs
import re
import requests
#Download and convert YT video
import youtube_dl
import time
#Get last song downloaded / delete last song/video
import shutil
import glob
import os
import sys
#Telegram Bot
import telebot
from telegram.ext import Updater
from telegram.ext import CommandHandler
#Get user settings
import json

# Telegram bot start
# Get the token in "token.json"
token = json.loads(open("token.json").read())
# Load bot with token
bot = telebot.TeleBot(token['token'])


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Benvenuto nel bot! Controlla /help per tutti i comandi a tua disposizione.\nInserisci il nome o l'url del video da scaricare:")

#Help commands

@bot.message_handler(commands=['help'])
def helpcommand(message):
	bot.reply_to(message, "/mp3 : I prossimi file verranno scaricati in formato mp3\n/mp4 : I prossimi file verranno scaricati in formato mp4")


@bot.message_handler(commands=['mp4'])
def mp4setting(message):
    def WritetoJSONFile(path, filename, data):
        filePathNameWExt = './' + filename
        with open(filePathNameWExt, 'w') as fp:
           json.dump(data, fp)

    filename = 'users.json'
    userid = message.chat.id;

    data = {}
    data['setting'] = 'mp4'
    data['userid'] = userid

    WritetoJSONFile('./',filename, data)

    bot.reply_to(message, "I prossimi file verranno scaricati in formato mp4!")
    print("Added 1 user preference to users.json")

@bot.message_handler(commands=['mp3'])
def mp3setting(message):

    def WritetoJSONFile(path, filename, data):
        filePathNameWExt = './' + filename
        with open(filePathNameWExt, 'w') as fp:
            json.dump(data, fp)

    filename = 'users.json'
    userid = message.chat.id;

    data = {}
    data['setting'] = 'mp3'
    data['userid'] = userid

    WritetoJSONFile('./',filename, data)

    bot.reply_to(message, "I prossimi file verranno scaricati in formato mp3!")
    print("Added 1 user preference to users.json")

#Download video/audio
@bot.message_handler(func=lambda message: True)
def echo_message(message):

    originalmessage = message.text
    #Replace spaces with -
    inputelement = originalmessage.replace(" ", "-")

    directlink = inputelement.startswith("https://")


    if directlink == True:
        #Print loading
        bot.reply_to(message, 'Ricerca del video... (10%)')

        ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': convertformat,
            'preferredquality': '192',
        }],
        }

        bot.reply_to(message, 'Download del video:\n' + inputelement + ' ...(30%)')

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([inputelement]) #Download the video
        bot.reply_to(message, 'Conversione e upload del video... (70%)')

        mp3_file = glob.glob("*.mp3")  #consider only files with .mp3 extension
        newest_file = max(mp3_file, key=os.path.getctime)  #get the last file
        file_title = os.path.splitext(newest_file)[0] #get the title of file
        audio = open(file_title + '.mp3', 'rb')
        bot.send_audio(message.chat.id, audio)

        #Delete last song / video downloaded
        audio.close()
        os.remove(file_title + '.mp3')

    if directlink == False:
        #Get html page of youtube
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + inputelement)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

        #Find video link
        complete_link = "https://www.youtube.com/watch?v=" + video_ids[0]   #Get the complete YT link

        bot.reply_to(message, 'Download del video:\n' + complete_link)
        bot.reply_to(message, '30%')

        #Get user preferences
        #Get user ID
        iduser = message.chat.id;
        #Open JSON file
        data = json.loads(open("users.json").read())

        if data["userid"] == iduser:
            if data["setting"] == "mp3":
                ydl_opts = {
                'format':"bestaudio/best",
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': "mp3",
                        'preferredquality': '192',
                    }],
                }
            else:
                ydl_opts = { }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([complete_link]) #Download the video
            meta = ydl.extract_info(complete_link)
            file_title = meta['title'] #get the title of file
            print(file_title)
            bot.reply_to(message, 'Conversione e upload del video... (70%)')

        if data["userid"] == iduser:
            if data["setting"] == "mp3":
                mp3_file = glob.glob("*.mp3")  #consider only files with .mp3 extension
                newest_file = max(mp3_file, key=os.path.getctime)  #get the last file
                os.rename(r"" + newest_file ,r"" + file_title + '.mp3') #Rename the file with real music title
                audio = open(file_title + '.mp3', 'rb')
                bot.send_audio(message.chat.id, audio)
            else:
                mp4_file = glob.glob("*.mp4")  #consider only files with .mp3 extension
                newest_file = max(mp4_file, key=os.path.getctime)  #get the last file
                file_title = os.path.splitext(newest_file)[0] #get the title of file
                video = open(file_title + '.mp4', 'rb')
                bot.send_video(message.chat.id, video)

        #Delete last song / video downloaded
        if data["setting"] == "mp3":
            audio.close()
            os.remove(file_title + '.mp3')
        else:
            video.close()
            os.remove(file_title + '.mp4')

        print("Last file: " + file_title + " Deleted!")


print("Bot Online!\nListening...")
bot.polling()
#print("Bot crashed\nRestarting...")
#os.system('python bot_main.py')


