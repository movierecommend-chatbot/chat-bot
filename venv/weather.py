from flask import Flask, request, jsonify, render_template, make_response, abort
from urllib.request import urlopen, Request
import json
import urllib
import bs4
from elasticsearch import Elasticsearch


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
@app.route('/weather', methods=['GET', 'POST'])
def webhook():

     # build a request object
    req = request.get_json(silent=True,force=True)

     # fetch action from json
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'json error'

    if action == 'get_results':
        res = results()
    elif action == 'weather':
        res = weather(req)
    else:
        log.error('Unexpected action')

    print('Action: ' + action)
    print('Response: ' + res)

    # return response
    return make_response(jsonify({'fulfillmentText': res}))

def weather(req):

    location = req['queryResult']['parameters']['geo-gu']

    print('dialogflow' + location + '!!!!!!!')

    enc_location = urllib.parse.quote(location + '+날씨')

    url = 'https://search.naver.com/search.naver?ie=utf8&query='+ enc_location

    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html,'lxml')


    #날씨에 따른 영화추천 코드







    return ('현재 ' + location + ' 날씨는 ' + soup.find('ul', class_='info_list').find('p', class_='cast_txt').text + '입니다.')

# run the app
if __name__ == '__main__':
   app.run()