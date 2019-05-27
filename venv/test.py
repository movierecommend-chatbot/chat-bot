import os
import sys
import urllib.request
client_id = "7pVG7KKXIzNPzgknhTAK"
client_secret = "c6MyifLd6W"
encText = urllib.parse.quote("007")
url = "https://openapi.naver.com/v1/search/movie.json?query=" + encText # json 결과
# url = "https://openapi.naver.com/v1/search/news.xml?query=" + encText # xml 결과
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)


response = urllib.request.urlopen(request)
rescode = response.getcode()
if(rescode==200):
    response_body = response.read().decode('utf-8')
    print(response_body)
else:
    print("Error Code:" + rescode)