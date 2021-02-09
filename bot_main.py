import urllib.request # Get Youtube html
from urllib.request import Request, urlopen
import lxml.html as LH
import re # Find all youtube IDs
import requests
import youtube_dl # Download and convert YT video
import time
import shutil # Get last song downloaded / delete last song/video
import glob
import os
import sys
import telebot # Telegram Bot
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import json # Get user settings
from mutagen.mp3 import MP3 # Insert song details
from mutagen.easyid3 import EasyID3
import mutagen.id3
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER
import numpy as np


# Telegram bot start
token = json.loads(open("token.json").read()) # Get the token in "token.json"
bot = telebot.TeleBot(token['token']) # Load bot with token

#---Commands---#
@bot.message_handler(commands=['start']) # Welcome command
def send_welcome(message):
	
    filename = 'users.json' 
    userid = str(message.chat.id)
    data[userid] = {'format' : 'mp3', 'basewebsite': 'ytm'} # Set default settings 
    WritetoJSONFile('./',filename, data)
    
    print("⚠️ Default config setting for the user: " + userid + " ⚠️") # Apply default download for user.
    
    bot.reply_to(message, "👋 Benvenuto nel bot! Ora tutti i contenuti che scaricherai saranno impostati di default con l'estensione .mp3\n🙋 Controlla /help per tutti i comandi a tua disposizione. \n✍️ Inserisci il nome o l'url del video da scaricare:")  # Start bot

@bot.message_handler(commands=['help']) # Help commands
def helpcommand(message):
	bot.reply_to(message, "/mp3 : I prossimi file verranno scaricati in formato mp3\n/mp4 : I prossimi file verranno scaricati in formato mp4\n/ytm : I prossimi file verranno scaricati da YouTube Music\n/yt : I prossimi file verranno scaricati da YouTube")


def WritetoJSONFile(path, filename, data):  # Access JSON
        filePathNameWExt = './' + filename
        with open(filePathNameWExt, 'w') as fp:
           json.dump(data, fp)
data = {} # Declare data
           
@bot.message_handler(commands=['mp4']) # Download msuic in .mp4 extension
def mp4setting(message):
    filename = 'users.json'
    userid = str(message.chat.id)
    try:
        if (data[userid]["basewebsite"]) == "yt":
            data[userid] = {"format" : "mp4", "basewebsite": "yt"}
        elif (data[userid]["basewebsite"]) == "ytm":
            data[userid] = {"format" : "mp4", "basewebsite": "ytm"}
        WritetoJSONFile('./',filename, data)
    except:
        data[userid] = {"format" : "mp4", "basewebsite": "ytm"}
        WritetoJSONFile('./',filename, data)

    bot.reply_to(message, "⚠️ I prossimi file verranno scaricati in formato mp4! ⚠️")
    print("⚠️ Edited configuration for the user: " + userid + " ⚠️")

@bot.message_handler(commands=['mp3']) # Download msuic in .mp3 extension
def mp3setting(message):
    filename = 'users.json'
    userid = str(message.chat.id)
    try:
        if (data[userid]["basewebsite"]) == "yt":
            data[userid] = {"format" : "mp3", "basewebsite": "yt"}
        elif (data[userid]["basewebsite"]) == "ytm":
            data[userid] = {"format" : "mp3", "basewebsite": "ytm"}
        WritetoJSONFile('./',filename, data)
    except:
        data[userid] = {"format" : "mp3", "basewebsite": "ytm"}
        WritetoJSONFile('./',filename, data)
        
    bot.reply_to(message, "⚠️ I prossimi file verranno scaricati in formato mp3! ⚠️")
    print("⚠️ Edited configuration for the user: " + userid + " ⚠️")
    
@bot.message_handler(commands=['yt']) # Download video/audio from Youtube
def ytsetting(message):
    filename = 'users.json'
    userid = str(message.chat.id)
    try:
        if (data[userid]["format"]) == "mp4":
            data[userid] = {"format" : "mp4", "basewebsite": "yt"}
        elif (data[userid]["format"]) == "mp3":
            data[userid] = {"format" : "mp3", "basewebsite": "yt"}
        WritetoJSONFile('./',filename, data)
    except:
        data[userid] = {"format" : "mp3", "basewebsite": "yt"}
        WritetoJSONFile('./',filename, data)
        
    bot.reply_to(message, "⚠️ I prossimi file verranno scaricati da YouTube! ⚠️")
    print("⚠️ Edited configuration for the user: " + userid + " ⚠️")
    
@bot.message_handler(commands=['ytm'])  # Download video/audio from Youtube Music
def ytmsetting(message):
    filename = 'users.json'
    userid = str(message.chat.id)
    try:
        if (data[userid]["format"]) == "mp4":
            data[userid] = {"format" : "mp4", "basewebsite": "ytm"}
        elif (data[userid]["format"]) == "mp3":
            data[userid] = {"format" : "mp3", "basewebsite": "ytm"}
        WritetoJSONFile('./',filename, data)
    except:
        data[userid] = {"format" : "mp3", "basewebsite": "ytm"}
        WritetoJSONFile('./',filename, data)

    bot.reply_to(message, "⚠️ I prossimi file verranno scaricati da YouTube Music! ⚠️")
    print("⚠️ Edited configuration for the user: " + userid + " ⚠️")

#---/Commands/---#


@bot.message_handler(func=lambda message: True) # Download video/audio
def echo_message(message):
            
    try: # Try to open JSON file
        data = json.loads(open("users.json").read())
    except:
        bot.reply_to(message, "❌ Errore interno del bot (LoadJSON Failed) ❌")
        sys.exit()
        os.system("python bot_main.py")
    
    originalmessage = message.text # Load title of video from telegram message  
    
    def download(downloadlink): # Download function
            try:
                if downloadlink.startswith("https://music.youtube.com"):
                    downloadlink.replace("&list=", "")
                    print(downloadlink)
                    
                userid = str(message.chat.id) #Get user ID                               
                iduser = message.chat.id # Get message ID       
                                 
                loadingmessage = bot.reply_to(message, '⚙️(30%) Download in corso...') # Print loading         
                messageid = loadingmessage.message_id
            
                    
                if (data[userid]["format"]) == "mp3":
                    ydl_opts = {
                    'format':"bestaudio/best",
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': "mp3",
                                'preferredquality': '192',
                            }],
                        }
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        
                        ydl.download([downloadlink]) #Download the video
                        meta = ydl.extract_info(downloadlink) # Extract link informations
                        
                        file_title = meta['title'] # Get file title
                        
                        file_author = meta['uploader'] # Get file author
                        bot.edit_message_text("⚙️(50%) Conversione e upload...",iduser, messageid)
                            
                    mp3_file = glob.glob("*.mp3")  #Consider only files with .mp3 extension
                    newest_file = max(mp3_file, key=os.path.getctime)  # Get the last file
                    
                    try:
                        os.rename(r"" + newest_file ,r"" + file_title + '.mp3') # Rename the file with real music title
                        
                        audio = EasyID3(file_title + ".mp3") # Insert audio metadata
                        audio['artist'] = file_author
                        audio['title'] = file_title
                        
                        audio.save() # Save audio metadata
                        bot.edit_message_text("⚙️(80%) Aggiungendo gli ultimi dettagli...",iduser, messageid)
                        
                        audio = open(file_title + '.mp3', 'rb') # Open & send song
                        bot.send_audio(message.chat.id, audio)
                        
                        os.remove(file_title + ".mp3") # Remove audio file
                        print("Last file: " + file_title + " Deleted!\n") # Print removed file
                        
                    except:
                        print("❌ Rename failed, sending original filename ❌")
                        
                        audio = EasyID3(newest_file) # Audio metadata
                        audio['artist'] = file_author
                        audio['title'] = file_title
                        
                        audio.save() # Save audio metadata
                        bot.edit_message_text("⚙️(80%) Aggiungendo gli ultimi dettagli...",iduser, messageid) # Details tg message
                        
                        audio = open(newest_file, 'rb') #Send song
                        bot.send_audio(message.chat.id, audio)
                                
                        audio.close() # Close audio file
                        os.remove(newest_file) # Remove audio file
                        print("Last file: " + newest_file + " Deleted!\n") # Print removed file
                            
                elif (data[userid]["format"]) == "mp4":
                    try:
                        ydl_opts = {
                        'format': 'bestvideo[ext=m4a]+bestaudio/best'
                        }
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            #Download the video
                            ydl.download([inputelement])
                            meta = ydl.extract_info(inputelement)
                            #Get file title
                            file_title = meta['title']
                            #Get file author
                            file_author = meta['uploader']
                        try:            
                            
                            bot.edit_message_text("⚙️ (70%) Conversione e upload del video...",iduser, messageid) # Loading message on Telegram bot
                            
                            mp4_file = glob.glob("*.mp4") # Consider only files with .mp4 extension
                            newest_file = max(mp4_file, key=os.path.getctime) # Get the last mp4 file
                            os.rename(r"" + newest_file ,r"" + file_title + '.mp4') #Rename the file with real music title
                            
                            video = open(file_title + '.mp4', 'rb') # Open & send .mp4 file
                            bot.send_video(message.chat.id, video)
                                    
                            video.close()
                            os.remove(file_title + '.mp4')

                            print("Last file: " + file_title + " Deleted!\n")
                        except:
                            print("❌ Rename failed, sending original filename ❌")
                            
                            audio = EasyID3(newest_file) # Audio metadata
                            audio['artist'] = file_author
                            audio['title'] = file_title
                            
                            audio.save() # Save audio metadata
                            bot.edit_message_text("⚙️(80%) Aggiungendo gli ultimi dettagli...",iduser, messageid) # Details tg message
                            
                            audio = open(newest_file, 'rb') #Send song
                            bot.send_audio(message.chat.id, audio)
                                    
                            audio.close() # Close audio file
                            os.remove(newest_file) # Remove audio file
                            print("Last file: " + newest_file + " Deleted!\n") # Print removed file
                    except: 
                        bot.edit_message_text("❌ Errore nel download del file video!",iduser, messageid) # Error message TG
            except:
               print("❌ Unknown Error")
       
    inputelement = originalmessage.replace(" ", "+") # Replace spaces with +   
    directlink = inputelement.startswith("https://") # Check if the input is a directlink
               
    if directlink == True: # If user inserted                
        download(directlink) # Download with var "directlink"

    if directlink == False:
        #Get html page of youtube
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + inputelement) # Get the complete YT Link
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode()) # Scraping informations

        #Find video link
        complete_link = "https://www.youtube.com/watch?v=" + video_ids[0]   # Get the complete YT link
        bot.reply_to(message, '🚀 Corrispondenza migliore:\n' + complete_link) # Print the video/music link
        download(complete_link) # Download with var "complete_link"

print("Bot Online! 🚀")
bot.polling()
