import re
from datetime import datetime, tzinfo, timedelta
import os
import requests
from requests.exceptions import URLRequired
import random
import time

class Zone(tzinfo):
    def __init__(self,offset,isdst,name):
        self.offset = offset
        self.isdst = isdst
        self.name = name
    def utcoffset(self, dt):
        return timedelta(hours=self.offset) + self.dst(dt)
    def dst(self, dt):
        return timedelta(hours=1) if self.isdst else timedelta(0)
    def tzname(self,dt):
        return self.name

loc = 'Shenzhen'

def get_activities():
    '''
    Get the latest 3 activities from activities.txt

    '''
    lines = open('activities.txt').readlines()
    arr = []
    for line in lines[:3]:
        li = line.strip().split('|')
        s = f"- {li[0]} - <a href='{li[2]}' target='_blank'>{li[1]}</a><br>"
        arr.append(s)
    acts = '\n'.join(arr)
    return acts
    
def get_weathernow():
    openweather_key = os.getenv('OPENWEATHER_KEY')
    apistr = f"http://api.openweathermap.org/data/2.5/weather?q={loc}&appid={openweather_key}&units=metric"
    weather = requests.get(apistr).json()

    feels_like = f"{weather['main']['feels_like']:.1f}"

    wind_speed = f"{weather['wind']['speed']:.1f}"

    description = weather["weather"][0]["description"]

    CNT = Zone(8, False, 'CNT')
    local_datetime = datetime.now(CNT).strftime('%m/%d/%Y %H:%M')
    w = f'''<p align="center">As of last update, the weather in {loc} :- <br>
It is {feels_like} &#8451;, {description}<br>
Wind speed is {wind_speed} m/s<br>
Local date time is {local_datetime}<br></p>'''
    return w

def get_pictures():
    unsplash_key = os.getenv('UNSPLASH_KEY')
    orientation = "portrait" if random.random() < 0.5 else "landscape"
    print(f"Picture orientation: {orientation}")
    apistr = f"https://api.unsplash.com/photos/random?query=china-architecture&orientation={orientation}&count=3&client_id={unsplash_key}"
    tries = random.randint(1, 5)
    for i in range(tries):
        print(f"Try: {i}")
        pic_result = requests.get(apistr).json()
        time.sleep(2)

    pictures = []
    for pic in pic_result:
        c =  pic['location']['city'] if pic['location']['country'] == 'China' and pic['location']['city'] != None else ''
        tmp = {'width': 200, 'height': round(pic['height'] / (pic['width'] / 200)), 'url': pic['urls']['thumb'], 'city': c}
        pictures.append(tmp)
    
    pictures = sorted(pictures, key=lambda k: k['height'])
    h = pictures[0]['height']
    imgs = ""
    for pic in pictures:
        if pic['city'] != '':
            tmp = f"<img width=\"{pic['width']}\" height=\"{h}\" src=\"{pic['url']}\" title=\"City: {pic['city']}\" /> "
        else:
            tmp = f"<img width=\"{pic['width']}\" height=\"{h}\" src=\"{pic['url']}\" /> "

        imgs = imgs + tmp

    return f'<p>{imgs}</p>'

def get_datetimenow():
    now = datetime.utcnow()
    return f"<p align=\"center\" style=\"font-size:90%\">This README was last updated at {now.strftime('%m/%d/%Y %H:%M')} UTC by Github Actions</p>"

def update_me(section, me, contents):
    reexp = f"(?P<Part1><!-- {section} start -->\n)(?P<Part2>[\s\S]+)(?P<Part3><!-- {section} end -->)"
    return re.sub(reexp, f"\g<Part1>{contents}\g<Part3>", me)

if __name__ == '__main__':
    me = ''.join(open('README.md').readlines())

    acts = get_activities()
    newme = update_me('Activities', me ,acts)
    me = newme

    dt = get_datetimenow()
    newme = update_me('Updatetime', me, dt)
    me = newme

    weather = get_weathernow()
    newme = update_me('Weather', me, weather)
    me = newme

    picture = get_pictures()
    newme = update_me('Picture', me, picture)
    me = newme

    with open('README.md', 'w') as fd_me:
        fd_me.write(me)