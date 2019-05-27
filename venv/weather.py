from flask import Flask, request, jsonify, render_template, make_response, abort
from urllib.request import urlopen, Request
import json
import urllib
import bs4
import random

import bio
import mvdata
# initialize the flask app
app = Flask(__name__)
log = app.logger


# default route
@app.route('/')
def index():
    return 'Hello World!!!!!!!!!'

# create a route for webhook
# @app.route('/webhook')
# def hello():
#     return 'Hello World!!'

def results():
    # return a fulfillment response
    return  ('This is a response from webhook.')

# create a route for webhook
@app.route('/webhook', methods=['POST','GET'])
def webhook():

     # build a request object
    req = request.get_json(silent=True,force=True)
    mvs=''
     # fetch action from json
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return nn

    if action == 'get_results':
        res = results()
    elif action == 'weather':
        location = req['queryResult']['parameters']['geo-gu']
        res = weather(location)
    elif action == 'weather.weather-yes':
        location = req['queryResult']['outputContexts'][1]['parameters']['geo-gu']
        res = recommend(location)

    elif action == 'bio':
        date = req['queryResult']['queryText']
        res = bio.bio(date)
    elif action == 'bio.bio-yes':
        date=req['queryResult']['outputContexts'][0]['parameters']['date.original'][0]
        res = bio.recommend(date)
    else:
        log.error('Unexpected action')

    print('Action: ' + action)
    print('Response: ' + res)

    # return response
    return make_response(jsonify({'fulfillmentText': res}))


def weather(location):


    print('dialogflow' + location + '!!!!!!!')

    enc_location = urllib.parse.quote(location + '+날씨')

    url = 'https://search.naver.com/search.naver?ie=utf8&query='+ enc_location

    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html,'lxml')


    return ('현재 ' + location + ' 날씨는 ' + soup.find('ul', class_='info_list').find('p', class_='cast_txt').text + '야, 맞니?')


def recommend(location):
    print('위치: '+location)

    #사용자 위치에 따른 날씨 type 추출
    res=weather(location)
    weather_type = res.split(' ')[3]
    print('사용자 위치에 따른 날씨: '+ weather_type)



    if weather_type == '맑음,':
        movie_type=random.choice(['animation','comedy','adventure','fantasy','drama','concert'])

    elif weather_type == '흐림,':
        movie_type=random.choice(['melo','horror','thrill','sf','criminal','drama'])
    elif weather_type == '구름,':
        movie_type=random.choice(['adventure','comedy','fantasy','melo','dacu','history','drama'])
    elif weather_type == '비,':
        movie_type=random.choice(['thrill','horror','war','criminal','family','drama','action'])
    elif weather_type == '눈.':
        movie_type=random.choice(['family','melo','comedy','action','drama'])
    else:
        movie_type='etc'

    rec_mv=mvdata.getMvdata(movie_type)


    return (rec_mv+', 이 영화 괜찮아?')





# run the app
if __name__ == '__main__':
   app.run()