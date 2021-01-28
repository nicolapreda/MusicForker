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
from fake_useragent import UserAgent


ua = UserAgent()

header = {'User-Agent':str(ua.chrome)}
ytmreq = Request("https://music.youtube.com/watch?v=I5V7igjZlVI&list=RDAMVMI5V7igjZlVI",headers=header)
webpage1 = urlopen(ytmreq).read().decode()
print(webpage1)
searchname = re.compile('<img id="img" class="style-scope yt-img-shadow" alt="" width="1048" src="https://lh3.googleusercontent.com/C1kJNdZQdjxxXJzUTrvd2w0YQGkCf1yxPWMy8IuMyxzSQJPBax6qcYkS2XSc0gs8u_WLuix0d6IJqiHF=w544-h544-l90-rj">', re.IGNORECASE | re.DOTALL )
copertina = re.findall(searchname, webpage1)
print(copertina)