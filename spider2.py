import requests
import json
import os

def getContent(url):
   header = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
   }
   try:
      r = requests.get(url,headers = header)
      return r.text
   except:
      r = requests.get(url,headers = headers,timeout=30)  
      return r.text

def create_bangumi_list():
   url = 'https://bangumi.bilibili.com/web_api/season/index_global?page=0'
   season_url = 'https://bangumi.bilibili.com/web_api/get_ep_list?season_id='
   re = getContent(url)
   f = open("./bangumi.json", "wb")
   f.write(re)
   f.close()
   bangumi_list = json.loads(re)
   l = len(bangumi_list['result']['list'])
   season_id_list = []
   anime_name_list = []
   url_list = []
   for i in range(l):
      anime_name = bangumi_list['result']['list'][i]['title']
      anime_name_list.append(anime_name)
      season_id = bangumi_list['result']['list'][i]['season_id']
      season_id_list.append(season_id)
      url = season_url + str(season_id_list[i])
      url_list.append(url)
   return anime_name_list,season_id_list,url_list

def get_cid_list(season_id_list,url_list):
   bangumi_cid_list = []
   for i in range(len(url_list)): 
      getContent(url_list[i])
      path = './bangumi/' + str(season_id_list[i]) + '.json'
      f = open(path, "wb")
      f.write(re)
      f.close()
      cid_list = json.loads(re)['result']
      print (cid_list)
      bangumi_cid_list.append(cid_list)
   return bangumi_cid_list

def getAllDmk(cid):
   dateUrl = 'http://comment.bilibili.com/rolldate,' + cid
   con = requests.get(dateUrl).content
   content=json.loads(con)
   for i in range(len(content)):
      timestamp = content[i]['timestamp']
      allUrl = 'http://comment.bilibili.com/dmroll,' + str(timestamp) + ',' + str(cid)
      dmk = getContent(allUrl)
      dmk = dmk.encode('utf8')
      f = open(cid + '-' + str(i) + '.xml','wb')
      f.write(dmk)
      f.close()

if __name__ == "__main__":
   anime_name_list,season_id_list,url_list = create_bangumi_list()
   bangumi_cid_list = get_cid_list(season_id_list, url_list)
   for i in range(bangumi_cid_list):
      for l in range(bangumi_cid_list[i]):
         getAllDmk(bangumi_cid_list[i][l])
'''
   dbpath = 'E:\\MongoDB\\bin'
   datapath = 'E:\\PythonProject\\dmksp\\bangumi.json'
   command = dbpath + '\\mongoimport.exe -d bangumi -c bangumi --type json --file ' + datapath
   os.system(command)
''' 