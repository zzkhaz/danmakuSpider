# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division
from StringIO import StringIO
from gzip import GzipFile
import gzip
import urllib2
import urllib
import zlib
import re
import os
import binascii 
import json

time = []              #弹幕出现的时间 以秒数为单位
dmkType = []           #弹幕的模式1..3 滚动弹幕 4底端弹幕 5顶端弹幕 6.逆向弹幕 7精准定位 8高级弹幕
size = []              #字号， 12非常小,16特小,18小,25中,36大,45很大,64特别大
color = []             #字体的颜色 以HTML颜色的十位数为准
timeStamp = []         #Unix格式的时间戳 基准时间为 1970-1-1 08:00:00
poolType = []          #弹幕池 0普通池 1字幕池 2高级弹幕
senderId = []          #发送者的ID
rowID = []             #弹幕在弹幕数据库中rowID
emotionLvl = []        #情感等级

def getContent(url):
	request = urllib2.Request(url)
	request.add_header('Accept-encoding', 'gzip,deflate')
	request.add_header('User-Agent',"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36")
	response = urllib2.urlopen(request)
	content = response.read()
	encoding = response.info().get('Content-Encoding')
	if encoding == 'gzip':
		content = fgzip(content)
	elif encoding == 'deflate':
		content = fdeflate(content)
	return content

def fgzip(data):
	buf = StringIO(data)
	f = gzip.GzipFile(fileobj=buf)
	return f.read()

def fdeflate(data):
	try:
		return zlib.decompress(data, -zlib.MAX_WBITS)
	except zlib.error:
		return zlib.decompress(data)

def getCid1(aid):
	url = 'http://www.bilibili.com/video/av' + aid
	html = getContent(url)
	cidlist = re.findall(".*cid[=](.*)[&]aid.*",html)
	cid =  ''.join(cidlist)
	return cid

def getCid2(aid):
	jjurl = 'http://www.jijidown.com/video/av' + aid
	jjhtml = getContent(jjurl)
	cidlist = re.findall(".*xml[&]cid[=](.*)[&]n[=].*",jjhtml)
	cid =  ''.join(cidlist)
	return cid
	
def getName(aid):
	url = 'http://www.bilibili.com/video/av' + aid
	html = getContent(url)
	namelist = re.findall("<title>(.*)</title>",html)
	name = str(namelist).decode('string_escape')
	return name

def getDmk(cid):
	DmkUrl = ('http://comment.bilibili.com/'+ cid +'.xml')
	print DmkUrl
	dmk = getContent('http://comment.bilibili.com/'+ cid +'.xml')	
	f = open(cid + '.xml','wb')
	f.write(dmk)
	f.close()

def getDmklist(data):
	dmklist = re.findall(".*[>](.*)[<].*",data)
	return dmklist

def getParameter(data):
	parameterlist = re.findall(".*p[=]\"(.*)\"[>].*",data)
	for i in range(len(parameterlist)):
		parameter = [str(x).decode('string_escape') for x in parameterlist[i].split(',')]
		time.append(parameter[0])
		dmkType.append(parameter[1])
		size.append(parameter[2])
		color.append(parameter[3])
		timeStamp.append(parameter[4])
		poolType.append(parameter[5])
		senderId.append(parameter[6])
		rowID.append(parameter[7])

def toJson(cid):
	f = open(cid + '.xml','rU')
	data = f.read()
	dmklist = re.findall(".*[>](.*)[<].*",data)
	parameterlist = re.findall(".*p[=]\"(.*)\"[>].*",data)
	for i in range(len(parameterlist)):
		parameter = [str(x).decode('string_escape') for x in parameterlist[i].split(',')]
		time.append(parameter[0])
		dmkType.append(parameter[1])
		size.append(parameter[2])
		color.append(parameter[3])
		timeStamp.append(parameter[4])
		poolType.append(parameter[5])
		senderId.append(parameter[6])
		rowID.append(parameter[7])
	f.close()
	f = open(cid + '.json', 'a+')
	for i in range(len(parameterlist)):		
		if i == 0:
			f.write('[')
		dmkDic = {'time': time[i],'dmkType': dmkType[i],'size': size[i],'color': color[i],'timeStamp': timeStamp[i],'poolType': poolType[i],'senderId': senderId[i],'rowID': rowID[i],'emotionLvl': '0','dmk': dmklist[i]}
		txt = json.dumps(dmkDic, encoding="UTF-8", ensure_ascii=False)
		f.write(json.dumps(txt))
		if i != len(dmklist)-1:
			f.write(',')
		if i == len(dmklist)-1:
			f.write(']')
	f.close()

def getDmkText(cid):
	f = open(cid + '.xml','rU')
	data = f.read()
	dmklist = re.findall(".*[>](.*)[<].*",data)
	f = open(cid + '.txt', 'a+')
	for i in range(len(dmklist)):
		dmkDic = {'dmk': dmklist[i]}
		f = open(cid + '.txt', 'a+')
		f.write(dmklist[i])
		f.write('\n')
	f.close()		

def downloadDMK(aid):
#       cid = getCid1(aid)
        cid = getCid2(aid)
	getDmk(cid)
	toJson(cid)
	getDmkText(cid)
	
def main():
	aid = str(input("please input av number:"))
        downloadDMK(aid)

if __name__ == '__main__':
	main()

