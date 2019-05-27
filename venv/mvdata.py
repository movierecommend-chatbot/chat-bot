from elasticsearch import Elasticsearch

import img

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
    return (mvdata + '\n- 포스터링크: ' + mvlink)

