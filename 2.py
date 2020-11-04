import browser_cookie3
import requests
import json
from discord_webhook import DiscordWebhook
from lxml import html
from time import sleep
import array as arr
import pytz
from datetime import datetime
import urllib3
#from Crypto.Cipher import AES
#from Crypto.Protocol.KDF import PBKDF2
#import keyring
#from os import getenv, path
#import sqlite3
import os
import http.cookiejar
import sqlite3
import http.cookiejar as cookielib

urllib3.disable_warnings()

tz = pytz.timezone('Asia/Kolkata')
time_now = datetime.now(tz).hour
explore_headers =  { 
                'Host': 'www.fiverr.com',
                'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Mobile Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US;q=0.7,en;q=0.3',
                'Accept-Encoding': 'gzip, deflate, br',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://www.fiverr.com/',
                'Connection': 'keep-alive'
                }
x_path = '//*[@id="main-wrapper"]/div[2]/section/div/article/div[1]/ul/li[1]/a'
response = None

def send_to_discord(data, profile_name):
    url = 'https://discord.com/api/webhooks/770637780384088086/xkiDEexpFIlre2GHXqBAyqLU7CVfMID47SevjmxRsF28wEaQiDO-ZI3KXdU1jzpO7QgZ'
    try:
        data = data+' requests from '+profile_name
        discord_alert = DiscordWebhook(url=url, content=data)
        response = discord_alert.execute()
        return True
    except Exception as e:
        print(e)
        return False


def get_cookies(cj, ff_cookies):
    con = sqlite3.connect(ff_cookies)
    cur = con.cursor()
    cur.execute("SELECT host, path, isSecure, expiry, name, value FROM moz_cookies")
    for item in cur.fetchall():
        c = cookielib.Cookie(0, item[4], item[5],
            None, False,
            item[0], item[0].startswith('.'), item[0].startswith('.'),
            item[1], False,
            item[2],
            item[3], item[3]=="",
            None, None, {})
        print(c)
        cj.set_cookie(c)

def index(profile_name, url):
    import sys
    cj = http.cookiejar.CookieJar()
    ff_cookies = "./{nos}/cookies.sqlite"
    cookies = get_cookies(cj, ff_cookies.format(nos=profile_name))
    s = requests.Session()
    s.cookies = cj
    
    req = s.get(url, verify=False, headers=explore_headers, cookies=cookies)
    if req.status_code == 200:
        tree = html.fromstring(req.content)
        t = tree.xpath(x_path)     
        data = t[0].attrib['data-count'] 
        if data != 0:
            send_to_discord(data, profile_name)
        else:
            pass
    else:
        raise requests.HTTPError(str(req.status_code))
    return True

while True:
    if ( time_now >= 8 ) and ( time_now <= 21 ):
        #urls = [['the_trained_one', 'https://www.fiverr.com/users/the_trained_one/requests']]
        urls = [['dapp_developer', 'https://www.fiverr.com/users/dapp_developer/requests']]
        
        for i in range(0, len(urls)):
            index(urls[i][0], urls[i][1])
        sleep(1800)
    else:
        sleep(11*60*60)
        print('pass')
        pass

