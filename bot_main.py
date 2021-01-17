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
	bot.reply_to(message, "/impostazioni : Configurazione del bot\n")

#Settings
@bot.message_handler(commands=['impostazioni'])
def send_welcome(message):
	bot.reply_to(message, "/mp3 : I prossimi file verranno scaricati in formato mp3\n/mp4 : I prossimi file verranno scaricati in formato mp4")


@bot.message_handler(commands=['mp4'])
def send_welcome(message):
    bot.reply_to(message, "I prossimi file verranno scaricati in formato mp4!")
    convertformat = 'mp4'
    return convertformat
@bot.message_handler(commands=['mp3'])
def send_welcome(message):
    bot.reply_to(message, "I prossimi file verranno scaricati in formato mp3!")
    convertformat = 'mp3'
    return convertformat

#Download video/audio
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    convertformat = 'mp3'
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
        ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': convertformat,
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
        print("Last file: " + file_title + " Deleted!")


print("Bot Online!\nListening...")
try:
    bot.polling()
except:
    print("Bot crashed\nRestarting...")
    os.system('python bot_main.py')


