#Get Youtube html
import urllib.request
from urllib.request import Request, urlopen
import lxml.html as LH
from requests_html import HTMLSession


#Find all youtube IDs
import re
import requests
import requests_html

#Download and convert YT video
import youtube_dl
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
session = HTMLSession()
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' }
ytmreq = Request("https://music.youtube.com/watch?v=I5V7igjZlVI&list=RDAMVMI5V7igjZlVI",headers=header)
webpage1 = urlopen(ytmreq).read().decode()
searchname = re.compile('<img id="img" class="style-scope yt-img-shadow" alt="">', re.IGNORECASE | re.DOTALL)
copertina = re.findall(searchname, ytmreq)

dreamsub_list = []
for i in copertina:
    k = i.replace(' ','-')
    dreamsub_list.append(k)

    #Show all watched anime
print(dreamsub_list)



