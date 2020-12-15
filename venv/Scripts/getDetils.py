# 获取具体物品
from bs4 import BeautifulSoup
import requests
import json
import sqlite3
import datetime
import sys
import re
import time

Cookie =  '_ntes_nuid=2aa8fb388a7d8dfcfe20f327b610e18a; Device-Id=E7Rl8bWbReoXkkr01PaU; _ga=GA1.2.962472406.1581387431; _ntes_nnid=2aa8fb388a7d8dfcfe20f327b610e18a,1605586644238; vinfo_n_f_l_n3=016860df49e4873d.1.0.1606819597564.0.1606820533516; NTES_CMT_USER_INFO=308308942%7C%E6%9C%89%E6%80%81%E5%BA%A6%E7%BD%91%E5%8F%8B0io6Le%7Chttp%3A%2F%2Fcms-bucket.nosdn.127.net%2F2018%2F08%2F13%2F078ea9f65d954410b62a52ac773875a1.jpeg%7Cfalse%7CeWQuYmUwMTYwMDI2Y2I5NDI0NmJAMTYzLmNvbQ%3D%3D; _gid=GA1.2.705940788.1607955127; game=csgo; Locale-Supported=zh-Hans; NTES_YD_SESS=.p5R1XzcUakBFBwT34SEI0W4mECxJ9hFvCjPi.7uYazgmVb8mPEkn1.1PXdjYd_r_AIdZz4Q3WTczvdrd6AXODz03EWdWOi3H1U.TcORFTjW0i6.H6knExzxg8hBDflxorb8zXAvUW18bJ3R4ekAN2Rb5vhOj5GqSilg.SEKmvG_sCsUtQafECZ_24CIMrMnpjwO42ARbj6VJm6UWsx2fh7MyhOHr3Y32ev3DBqzdSu9t; S_INFO=1608026411|0|3&80##|17640033514; P_INFO=17640033514|1608026411|1|netease_buff|00&99|null&null&null#lin&210100#10#0|&0|null|17640033514; remember_me=U1092697961|xEP3UzjTH2pH7eu8Qh4FQ66qeseKgnUo; session=1-VOZIHo0uC8XcqvmTbV3gc_MKgc_2IXgkSWaBG_ZpAboT2045747249; _gat_gtag_UA_109989484_1=1; csrf_token=IjViZDU3Y2EyYmZjNGI5YWFjMzFiOGM2MjRiYTgyMzM5ZWMwNDEwNTAi.EroasA.YOaKkjFATb68AYVOzpYu0pOgBTE'

DollarScale=0.8
now=datetime.datetime.now()
nowString = now.strftime("%Y-%m-%d %H:%M:%S")
conn = sqlite3.connect("database.db")
print(conn)
c = conn.cursor()
pageCount=0


#创建sqlite表,如果已经存在则跳过
sql='''
create table buff
       (id int primary key not null,
        name text,
        scale_buff2steam  real,
        scale_steam2buff  real,
        minus_steam2buff real,
        steam_min_price real,
        buff_min_price real,
        buffonSale int,
        buffBuy int,
        buy_max_price real,
        exterior text,
        type text,
        category_group text,
        steam_market_link text,
        time  text
        );
 '''



try:
  c.execute(sql) # 执行sql语句
  conn.commit()  # 提交数据库操作
  print("数据库创建成功！")
except (sqlite3.OperationalError):
  print("数据库开启成功！")
  pass

def fork():
    print("buck")

def setCookie(cookie):
    "设置cookie"
    global Cookie
    Cookie = cookie.strip('\n')
def printCookie():
    print(Cookie)
def setDollarScale(scale2Search):
    global DollarScale
    DollarScale = scale2Search

def search(url,categoType):
      "遍历大类下全部物品"
      global pageCount
      url = url
      headers = {
          'Cookie': Cookie
      }
      response = requests.get(url, headers=headers)
      try:
        content = json.loads(response.text)
        pageCount=pageCount+1
        print("当前待爬取url", url)
      except json.decoder.JSONDecodeError:
        print("429请求次数过多,已搜索页面数:",pageCount)
        print("------------当前待爬取url",url)
        time.sleep(10)
        return


      #print("--------------------------------------具体信息---------------------------------------------------------")
      for i in range(20):
          #变量定义区
          item = content['data']['items'][i]
          id=item['id']                                 #物品steam市场id
          name = item['name']                           #物品名称
          buffMinPrice = float(item['sell_min_price'])       #buff底价
          steamMinPrice = float(item['goods_info']['steam_price_cny'])  #steam底价
          scale = round(float(item['sell_min_price']) / (float(item['goods_info']['steam_price_cny']) * 0.87), 4)  #挂刀比例
          minus_steam2buff = round((buffMinPrice * 0.965-(steamMinPrice * float(DollarScale))),2) # 扫货差价
          scaleSteam2Buff = round(minus_steam2buff/(steamMinPrice* float(DollarScale)),4)# 扫货收益率
          buffonSale = item['sell_num']  #buff在售数量
          buffBuy = item['buy_num']  #buff求购数量
          type = item['goods_info']['info']['tags']['quality']['localized_name']   #是否为暗金/纪念品
          buyMaxPrice = item['buy_max_price']  #求购最高价
          try:
              exterior = item['goods_info']['info']['tags']['exterior']['localized_name']  #磨损等级
          except KeyError:
              exterior = 1;
          steamMarketLink = item['steam_market_url'] #steam市场URL
          category_group = {'knife':'匕首','pistol':'手枪','rifle':'步枪','smg':'微型冲锋枪','shotgun':'霰弹枪','machinegun':'机枪','hands':'手套','sticker':'印花','other':'其他'}
          categoTypeInside = category_group[categoType]



          #print("ID:{id}\tBuff最低售价：{buffMinPrice}\tsteam最低售价(换算前):{steamMinPrice}\t比例:{scale}".format(id=name,buffMinPrice=buffMinPrice,steamMinPrice=steamMinPrice,scale=scale))
          #赋值区
          try:
            sql = "insert into buff values({id},'{name}',{scale},{scaleSteam2Buff},{minus_steam2buff},\
            {steamMinPrice},{buffMinPrice},{buffonSale},{buffBuy},{buyMaxPrice},'{exterior}','{type}','{categoryGroup}','{steamMarketLink}','{time}')".format \
                  (id=id, name=name, buffMinPrice=buffMinPrice, steamMinPrice=steamMinPrice, scale=scale,
                   scaleSteam2Buff=scaleSteam2Buff,
                   minus_steam2buff=minus_steam2buff, buffonSale=buffonSale, buffBuy=buffBuy, type=type,
                   buyMaxPrice=buyMaxPrice, exterior=exterior,categoryGroup=categoTypeInside,
                   steamMarketLink=steamMarketLink, time=nowString)
            #print(sql)
            c.execute(sql)  # 执行sql语句
            conn.commit()  # 提交数据库操作
          except sqlite3.IntegrityError:
            sql="update buff set name='{name}',buff_min_price={buffMinPrice},steam_min_Price={steamMinPrice},\
            scale_steam2buff={scaleSteam2Buff},minus_steam2buff={minus_steam2buff},buffonSale={buffonSale},buffBuy={buffBuy},\
            type='{type}',buy_max_price={buyMaxPrice},exterior='{exterior}',category_group='{categoryGroup}',steam_market_link='{steamMarketLink}',\
            time='{time}',scale_buff2steam={scale} where id={id}".format \
                (id=id, name=name, buffMinPrice=buffMinPrice, steamMinPrice=steamMinPrice, scale=scale,
                 scaleSteam2Buff=scaleSteam2Buff,
                 minus_steam2buff=minus_steam2buff, buffonSale=buffonSale, buffBuy=buffBuy, type=type,
                 buyMaxPrice=buyMaxPrice, exterior=exterior,categoryGroup=categoTypeInside,
                 steamMarketLink=steamMarketLink, time=nowString)
            #print(sql)
            c.execute(sql)  # 执行sql语句
            conn.commit()  # 提交数据库操作
          #键值错误处理，调试中



      return

def urlAnalyze(categoType):
  "URL解析，由大类页面分析该大类消息"
  #print(categoType)
  url = ("https://buff.163.com/api/market/goods?game=csgo&page_num=1&category_group=%s&_=1607400865227") % categoType
  print(Cookie)
  headers = {
      'Cookie': Cookie
  }
  response = requests.get(url, headers=headers)
  content = json.loads(response.text)
  if (content['code']=='OK'):
    print("-----------------------------------该类物品统计信息------------------------------------------------------")
    print('目前统计的类型为：'+content['data']['items'][0]['goods_info']['info']['tags']['type']['localized_name'])
    print('buff上共有',content['data']['total_count'],'件在售/',content['data']['total_page'],'页')
    #遍历大类下全部物品
    for i in range(1,content['data']['total_page']):
        #url=("https://buff.163.com/api/market/goods?game=csgo&page_num=%d&category_group=shotgun&_=1607400865227")%i
        url = ("https://buff.163.com/api/market/goods?game=csgo&page_num={}&category_group={}&_=1607400865227".format(i,url))
        search(url,categoType)
  else:
      print("-----------------------------------获取物品大类信息失败------------------------------------------------------")
      print(content)
      return

def getAllDetils():
    print("cookie:" + Cookie)
    print('Dollar:' , DollarScale)
    url={0:'knife',1:'pistol',2:'rifle',3:'smg',4:'shotgun',5:'machinegun',6:'hands',7:'sticker',8:'other'}
    for i in range(0,9):
      urlAnalyze(url[i])


if __name__ == '__main__':
  #url= 'shotgun'
  #urlAnalyze(url)
  getAllDetils()
  print(c.execute('select id from buff'))
