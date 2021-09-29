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
    
if __name__ == '__main__':
    print(get_activities())