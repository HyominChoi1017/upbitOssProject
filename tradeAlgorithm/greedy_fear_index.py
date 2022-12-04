import datetime
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

def fear_last_6month():

    url = ' https://api.alternative.me/fng/?limit=0'
    data = requests.get(url).json()
    value = []
    time = []
    for i in data['data']:
        value.append(i['value'])
        time.append(datetime.datetime.fromtimestamp(int(i['timestamp'])).strftime('%Y-%m-%d'))
    value = value[::-1]
    time = pd.to_datetime(time[::-1])
    fng = pd.Series(value,time,name='fngIndex')

    return pd.DataFrame(fng[-8:])


# 공포불안지수에도 RSI를 넣을까?
'''
data = fear_last_6month()['fngIndex']
maxx = -1
minn = 999
total = 0

print(data)

for d in data:
    d = int(d)
    if maxx < d:
        maxx = d
    if minn > d:
        minn = d
    total += d 
print('{} {} {}'.format(maxx, minn, total/len(data)))
'''