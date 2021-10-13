import re
from datetime import datetime, tzinfo, timedelta
import os
import requests

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
    w = f'''As of last update, the weather in {loc} :- <br>
It is {feels_like} &#8451;, {description}<br>
Wind speed is {wind_speed} m/s<br>
Local date time is {local_datetime}<br>'''
    return w

def get_datetimenow():
    now = datetime.utcnow()
    return f"This README was last updated at {now.strftime('%m/%d/%Y %H:%M')} UTC by Github Actions"

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

    with open('README.md', 'w') as fd_me:
        fd_me.write(me)