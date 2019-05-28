from flask import Flask, request, jsonify, render_template, make_response, abort
from urllib.request import urlopen, Request
import json
import urllib
import bs4
import random
from elasticsearch import Elasticsearch

import bio
import img

# initialize the flask app
app = Flask(__name__)
log = app.logger
es = Elasticsearch(hosts="127.0.0.1", port=9200)



# default route
@app.route('/')
def index():
    return 'Hello World!'


# create a route for webhook
@app.route('/webhook')
def hello():
    return 'Hello World!!'


def results():
    # return a fulfillment response
    return ('This is a response from webhook.')


# create a route for webhook
@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    # build a request object
    req = request.get_json(silent=True, force=True)
    mvs = ''
    # fetch action from json
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'json error'

    if action == 'get_results':
        res = results()

    elif action == 'weather':
        location = req['queryResult']['parameters']['geo-gu']
        res = weather(location)

    elif action == 'weather.weather-yes':
        location = req['queryResult']['outputContexts'][1]['parameters']['geo-gu']
        print('위치 !! ' + location)
        res = recommend(location)


    elif action == 'bio':
        date = req['queryResult']['queryText']
        res = bio.bio(date)

    elif action == 'bio.bio-yes':
        date = req['queryResult']['outputContexts'][1]['parameters']['date.original'][0]
        res = bio.recommend(date)

    elif action == 'MovieStory':
        print('story!!' + movieName)
        res = MovieStory(movieName)

    elif action == 'MovieActor':
        res = MovieActor(movieName)

    elif action == 'MovieRating':
        res = MovieRating(movieName)

    else:
        log.error('Unexpected action')

    print('Action: ' + action)
    print('Response: ' + res)

    # return response
    return make_response(jsonify({'fulfillmentText': res}))


def weather(location):
    enc_location = urllib.parse.quote(location + '+날씨')

    url = 'https://search.naver.com/search.naver?ie=utf8&query=' + enc_location

    req = Request(url)
    page = urlopen(req)
    html = page.read()
    soup = bs4.BeautifulSoup(html, 'lxml')

    return ('현재 ' + location + ' 날씨는 ' + soup.find('ul', class_='info_list').find('p',
                                                                                  class_='cast_txt').text + '야, 맞니?')


def recommend(location):
    print('위치: ' + location)

    # 사용자 위치에 따른 날씨 type 추출
    res = weather(location)
    weather_type = res.split(' ')[3]
    print('사용자 위치에 따른 날씨: ' + weather_type)

    if weather_type == '맑음,':
        movie_type = random.choice(['animation', 'comedy', 'adventure', 'fantasy', 'drama', 'concert'])

    elif weather_type == '흐림,':
        movie_type = random.choice(['melo', 'horror', 'thrill', 'sf', 'criminal', 'drama'])
    elif weather_type == '구름,':
        movie_type = random.choice(['adventure', 'comedy', 'fantasy', 'melo', 'dacu', 'history', 'drama'])
    elif weather_type == '비,':
        movie_type = random.choice(['thrill', 'criminal', 'family', 'drama', 'action'])
    elif weather_type == '눈.':
        movie_type = random.choice(['family', 'melo', 'comedy', 'action', 'drama'])
    else:
        movie_type = 'etc'

    rec_mv = getMvdata(movie_type)

    return (rec_mv + '\n영화 괜찮아?')


def getMvdata(type):
    es = Elasticsearch()

    res = es.search(
        index=type,
        body={

            "size": 1,
            "query": {
                "function_score": {
                    "query": {
                        "match_all": {}
                    },
                    "functions": [
                        {
                            "random_score": {}
                        }
                    ]
                }
            }
        }
    )
    mvs = res['hits']['hits'][0]['_source']
    print(mvs)

    mvdata = '- 영화제목: ' + str(mvs['movieNm']) + ' 장르: ' + str(mvs['genreAlt']) + ' 개봉상태: ' + str(
        mvs['prdtStatNm']) + ' 국가: ' + str(mvs['nationAlt']) + ' 개봉년도: ' + str(mvs['prdtYear'])

    mvlink = img.imgLink(mvs['movieNm'])
    global movieName
    movieName = mvs['movieNm']

    print(movieName)
    # moviename1 = str(mvs['movieNm'])
    # return (moviename1+'영화 이름임!!')
    return (mvdata + '\n- 포스터링크: ' + mvlink)


def MovieStory(cname):
    print(cname)
    name = urllib.parse.quote(cname)

    url2 = 'https://movie.naver.com/movie/search/result.nhn?query=' + name + '&section=all&ie=utf8'
    req2 = Request(url2)
    page2 = urlopen(req2)
    html2 = page2.read()
    soup2 = bs4.BeautifulSoup(html2, 'lxml')

    cs = soup2.find_all('p', attrs={'class': 'result_thumb'})

    link = cs[0].find('a')['href']

    realLink = urllib.parse.quote(link)

    url3 = 'https://movie.naver.com' + realLink

    req3 = Request(url3)
    page3 = urlopen(req3)
    html3 = page3.read()
    soup3 = bs4.BeautifulSoup(html3, 'lxml')

    movie_story = '- 줄거리 : ' + soup3.find('div', class_='story_area').find('p', class_='con_tx').text

    return (movie_story)


def MovieRating(cname):
    name = urllib.parse.quote(cname)

    url2 = 'https://movie.naver.com/movie/search/result.nhn?query=' + name + '&section=all&ie=utf8'
    req2 = Request(url2)
    page2 = urlopen(req2)
    html2 = page2.read()
    soup2 = bs4.BeautifulSoup(html2, 'lxml')

    movie_score = soup2.find('ul', class_='search_list_1').find('em', class_='num').text
    movie_score_return = '- 평점 : ' + repr(movie_score) + '점'

    return (movie_score_return)


def MovieActor(cname):
    name = urllib.parse.quote(cname)

    url2 = 'https://movie.naver.com/movie/search/result.nhn?query=' + name + '&section=all&ie=utf8'
    req2 = Request(url2)
    page2 = urlopen(req2)
    html2 = page2.read()
    soup2 = bs4.BeautifulSoup(html2, 'lxml')

    cs = soup2.find_all('p', attrs={'class': 'result_thumb'})

    link = cs[0].find('a')['href']

    realLink = urllib.parse.quote(link)

    url3 = 'https://movie.naver.com' + realLink

    req3 = Request(url3)
    page3 = urlopen(req3)
    html3 = page3.read()
    soup3 = bs4.BeautifulSoup(html3, 'lxml')

    movie_actor_list = soup3.find_all('div', attrs={'class': 'people'})
    movie_count = len(movie_actor_list)
    print(movie_count)
    for i in range(0, movie_count):
        movie_actor = movie_actor_list[i].find('a')['title']
        movie_actors = '- 배우/감독 : ' + movie_actor

    return (movie_actors)


# run the app
if __name__ == '__main__':
    app.run()