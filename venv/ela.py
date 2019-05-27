from elasticsearch import Elasticsearch
import urllib.request as ul
import json
import time
import csv

key = "d5ff14e5fa712e12dba02b7b8146f38e"


class ElaAPI:
    es= Elasticsearch()
    # es.indices.delete(index='index-test', ignore=[400, 404])

    @classmethod
    def insertIndex(cls):


        for j in range(69,100):
            url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=" + key + "&curPage=" + str(
                j)
            request = ul.Request(url)

            response = ul.urlopen(request)
            rescode = response.getcode()

            if (rescode == 200):
                responseData = response.read()

            result = json.loads(responseData)

            print(result)
            # for i in range(0,10):
            #     doc = {"moiveNm": result["movieListResult"]["movieList"][i]["movieNm"],
            #            "genreAlt": result["movieListResult"]["movieList"][i]["genreAlt"],
            #            "prdtYear": result["movieListResult"]["movieList"][i]["prdtYear"],
            #            "prdStat": result["movieListResult"]["movieList"][i]["prdtStatNm"]
            #            }
            #
            #     time.sleep(1)
            #     res=cls.es.index(index="index-test",doc_type='movie',id=(j-1)*10+i,body=doc)
            #     cls.es.indices.refresh(index="index-test")
            #     # res = es.get(index="index-test", doc_type='movie', id=1)
            #     # print(res['_source'])

    @classmethod
    def allIndex(cls):
        # Elasticsearch에 있는 모든 Index 조회
        print (cls.es.cat.indices())

    @classmethod
    def alldata(cls):

        for i in range(1,20):
            res=cls.es.get(index="index-test", doc_type="movie",id=i)
            print(res['_source'])

    @classmethod
    def transcsv(cls):
        data = cls.es.search(
            index="index-test",
            size=10000,
            body={
                "query": {
                    "match_all": {
                    }
                }
            }
        )

        csv_columns=['moiveNm','genreAlt','prdtYear','prdStat']
        csv_file='C:/Users/anyin/OneDrive/바탕 화면/movie.csv'

        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for document in [x['_source'] for x in data['hits']['hits']]:
                writer.writerow(document)


ElaAPI.allIndex()
# ElaAPI.insertIndex()
#ElaAPI.alldata()
# ElaAPI.transcsv()

