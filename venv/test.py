import bs4
from flask import Flask, request, jsonify, render_template, make_response, abort
from urllib.request import urlopen, Request
import urllib

def MovieStory(cname):
    print(cname)
    name = urllib.parse.quote(cname)

    url2 = 'https://movie.naver.com/movie/search/result.nhn?query=' + name + '&section=all&ie=utf8'
    req2 = Request(url2)
    page2 = urlopen(req2)
    html2 = page2.read()
    soup2 = bs4.BeautifulSoup(html2, 'lxml')

    cs = soup2.find_all('p', attrs={'class': 'result_thumb'})

    try:
        link = cs[0].find('a')['href']
    except:
        print('영화정보 없음')
        return ('영화정보 없음')

    realLink = urllib.parse.quote(link)

    url3 = 'https://movie.naver.com' + realLink

    req3 = Request(url3)
    page3 = urlopen(req3)
    html3 = page3.read()
    soup3 = bs4.BeautifulSoup(html3, 'lxml')

    try:
        movie_story = '- 줄거리 : ' + soup3.find('div', class_='story_area').find('p', class_='con_tx').text
    except:
        print('줄거리없음')
        return ('내용 없음')

    return (movie_story)


print(MovieStory('배스턴'))