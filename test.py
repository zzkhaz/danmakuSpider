# -*- coding: utf-8 -*-
import os # path manipulation
import urllib as urllib
import requests
import json
import re
from getDanmaku import *
#star_year 年份
#quarter 季度，1、2、3、4分别表示一月、四月、七月、十月新番
#version 类型，0-全部，1-TV版，2-OVA/OAD，3-剧场版，4-其他
#is_finish 状态，0-全部，1-连载，2-完结
#tag_id TAG
#area  地区，0-全部，1-国产，2-日本，3-美国，4-其他
#index_type 排序方式，0-更新时间，1-追番人数，2-开播时间
#index_short 排序顺序，0-降序，1-升序



def getBangumi(star_year,quarter,version,is_finish,area):
        path0 = './' + str(star_year) + '年第' + str(quarter) + '季度新番' + '/'
        os.mkdir(path0.decode("utf8").encode("gbk"))
        os.chdir(path0.decode("utf8").encode("gbk"))
	url = 'http://bangumi.bilibili.com/web_api/season/index?page=1&version=' + str(version) + '&is_finish=' + str(is_finish) + '&start_year=' + str(star_year)+ '&quarter=' + str(quarter) + '&tag_id=&area=' + str(area)
	con = requests.get(url).content
	content=json.loads(con,"utf-8")
	cont=len(content['result']['list'])
        for i in xrange(cont):
                anime = content['result']['list'][i]['title']
                #print '开始下载' + str(anime) + '的弹幕'
                anime = re.sub("[\s+\.\!\/_,$%^*(+\"\'\:]+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),anime)
                path = './' + anime + '/'  
                os.mkdir(path)
                animeId = str(content['result']['list'][i]['season_id'])
                getAvNum(animeId,path)
        parent_path = os.path.dirname(os.getcwd())
        os.chdir(parent_path)

def getAvNum(animeId,path):
        os.chdir(path)
        url = 'http://bangumi.bilibili.com/jsonp/seasoninfo/' + str(animeId) + '.ver'
        cont = requests.get(url).content
        if  cont.find('seasonListCallback')!=-1:
                rex = re.compile(r'\w+[(]{1}(.*)[)]{1}')
                con = rex.findall(cont)[0]
        else:
                con = cont
	content = json.loads(con,"utf-8")
	cont = len(content['result']['episodes'])
        for i in xrange(cont):
                index = content['result']['episodes'][i]['index']
                path2 = './' + index +'/'
                os.mkdir(path2)
                os.chdir(path2)
                aid = str(content['result']['episodes'][i]['av_id'])
                downloadDMK(aid)
                parent_path = os.path.dirname(os.getcwd())
                os.chdir(parent_path)
        parent_path = os.path.dirname(os.getcwd())
        os.chdir(parent_path)

def main():
	getBangumi(2016,1,1,0,2)
        
if __name__ == '__main__':
	main()


	
