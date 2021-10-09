import re
from datetime import datetime

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

    fd_me = open('README.md', 'w')
    fd_me.write(update_me('Activities', me, acts))
    fd_me.close()