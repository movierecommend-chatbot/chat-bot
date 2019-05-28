from flask import Flask, request, jsonify, render_template, make_response, abort
from urllib.request import urlopen, Request
import json
import urllib
import bs4
import random
import re

def imgLink(cname):
    name = urllib.parse.quote(cname)

    url2 = 'https://movie.naver.com/movie/search/result.nhn?query=' + name + '&section=all&ie=utf8'
    req2 = Request(url2)
    page2 = urlopen(req2)
    html2 = page2.read()
    soup2 = bs4.BeautifulSoup(html2, 'lxml')

    cs = soup2.find_all('p', attrs={'class':'result_thumb'})

    link = cs[0].find('a')['href']

    realLink = urllib.parse.quote(link)

    url3 = 'https://movie.naver.com' + realLink

    req3 = Request(url3)
    page3 = urlopen(req3)
    html3 = page3.read()
    soup3 = bs4.BeautifulSoup(html3, 'lxml')

    # 링크로 들어가서 포스터 확인(임의로)
    img = soup3.find('div', class_='poster').find('img')
    img_src = img.get('src')
    print(img_src)

    return (img_src)