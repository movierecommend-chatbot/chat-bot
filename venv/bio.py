from flask import Flask, request, jsonify, render_template, make_response, abort
from urllib.request import urlopen, Request
from datetime import date
import matplotlib.dates
from pylab import *
from numpy import array,sin,pi
import random

import img
import weather
# function for responses
def bio(dates):

    year = int(dates.split('-')[0])
    month = int(dates.split('-')[1])
    day = int(dates.split('-')[2])



    t0 = date(year, month, day).toordinal()
    t1 = date.today().toordinal()
    t = array(range((t1 - 10), (t1 + 10)))  # range of 20 days

    y = 100 * [sin(2 * pi * (t - t0) / 23),  # Physical
               sin(2 * pi * (t - t0) / 28),  # Emotional
               sin(2 * pi * (t - t0) / 33)];  # Intellectual

    # converting ordinals to date
    label = []
    for p in t:
        label.append(date.fromordinal(p))

    fig = figure()
    ax = fig.gca()
    plot(label, y[0], label, y[1], label, y[2])
    # adding a legend
    legend(['Physical', 'Emotional', 'Intellectual'])
    # formatting the dates on the x axis
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter('%d/%b'))

    # build a request object
    req = request.get_json(force=True)

    # fetch action from json
    action = req.get('queryResult').get('action')
    result = 0
    length = len(y[1])
    for i in y[1]:
        result += i

    result = result / length
    s = ''
    answer = random.randint(-99, 99)
    if answer < 0:
        s += '저조기'
    elif answer >= 1 and answer <= 67:
        s += '고조기'

    else:
        s += '위험일'
    print(answer)

    # return a fulfillment response
    return ('너의 감성 바이오 리듬은 '+str(answer)+'이고 '+str(s)+' , 맞니?')

def recommend(date):

    bios=bio(date)
    bioState=bios.split(' ')[5]
    print(bioState)

    if bioState == '저조기' or bioState == '위험일':
        movie_type=random.choice(['melo','horror','thrill','sf','criminal','drama','war','family','action'])
    elif bioState == '고조기':
        movie_type=random.choice(['animation','comedy','adventure','fantasy','drama','concert','melo','action'])
    else:
        movie_type = 'etc'

    rec_mv=weather.getMvdata(movie_type)

    return (rec_mv+', 이 영화 괜찮아?')
