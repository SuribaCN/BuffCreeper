# 获取具体物品
from bs4 import BeautifulSoup
import requests
import json
import sqlite3
import datetime
import sys
import re

Cookies =  '_ntes_nuid=2aa8fb388a7d8dfcfe20f327b610e18a; Device-Id=E7Rl8bWbReoXkkr01PaU; _ga=GA1.2.962472406.1581387431; _ntes_nnid=2aa8fb388a7d8dfcfe20f327b610e18a,1605586644238; vinfo_n_f_l_n3=016860df49e4873d.1.0.1606819597564.0.1606820533516; _gid=GA1.2.2117115307.1607343658; Locale-Supported=zh-Hans; NTES_YD_SESS=cM4.n_.8Z8KU6xdPhYohGimkvjHXOOtaCaXS1c.TplqY9dUy9SsiI2c2SGrXprnAn57rEqQ3OPzFqVrAre5GZNquOsPrPZ1OJ2WczFZ8bzXPu1ecJeiIsBqBYy_LNgRBHAUyqG5VWP2yUKO8Qji5to8UwV_ZXwhxCL0s5B8csKBylwyilnaI1Uc2eX.krYBaGeMqueBspELkmmtbeaB5rcC40_ZJAOpOojVONLxqrCTkv; S_INFO=1607352432|0|3&80##|17640033514; P_INFO=17640033514|1607352432|1|netease_buff|00&99|null&null&null#lin&210100#10#0|&0||17640033514; remember_me=U1092697961|CXDmKLWBaJt8fMsyhzxKegx3XzUFavgE; session=1-U2FiwbZG0Aydifzzp8CLPCMn-9KQ17DDYgKPHUIv7m5T2045747249; game=dota2; csrf_token=ImIzNGY2ZWU3NmIxNWRmYjliODAzMzY0NGEyMGFhYzM4ZjQ4MmMxMDYi.ErCPIA.rUMcvrOULToT8vG_1JSc1zjQzzo'

DollarScale=0.8
now=datetime.datetime.now()
nowString = now.strftime("%Y-%m-%d %H:%M:%S")
conn = sqlite3.connect("database.db")
print(conn)
c = conn.cursor()


#创建sqlite表,如果已经存在则跳过
sql='''
create table buff
       (id int primary key not null,
        name text,
        buff_min_price real,
        steam_min_price real,
        scale_buff2steam  real,
        scale_steam2buff  real,
        minus_steam2buff real,
        buffonSale int,
        buffBuy int,
        type text,
        buy_max_price real,
        exterior text,
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


def buck(str):
      "遍历大类下全部物品"
      url = str
      headers = {
          'Cookie': Cookies
      }
      response = requests.get(url, headers=headers)
      content = json.loads(response.text)


      print("--------------------------------------具体信息---------------------------------------------------------")
      for i in range(20):
          #变量定义区
          item = content['data']['items'][i]
          id=item['id']                                 #物品steam市场id
          name = item['name']                           #物品名称
          buffMinPrice = float(item['sell_min_price'])       #buff底价
          steamMinPrice = float(item['goods_info']['steam_price_cny'])  #steam底价
          scale = round(float(item['sell_min_price']) / (float(item['goods_info']['steam_price_cny']) * 0.87), 4)  #挂刀比例
          minus_steam2buff = round((buffMinPrice * 0.965-(steamMinPrice * DollarScale)),2) # 扫货差价
          scaleSteam2Buff = round((minus_steam2buff/(steamMinPrice * DollarScale)), 4)  # 扫货收益率
          buffonSale = item['sell_num']  #buff在售数量
          buffBuy = item['buy_num']  #buff求购数量
          type = item['goods_info']['info']['tags']['quality']['localized_name']   #是否为暗金/纪念品
          buyMaxPrice = item['buy_max_price']  #求购最高价
          try:
              exterior = item['goods_info']['info']['tags']['exterior']['localized_name']  #磨损等级
          except KeyError:
              exterior = 1;
          steamMarketLink = item['steam_market_url'] #steam市场URL



          #print("ID:{id}\tBuff最低售价：{buffMinPrice}\tsteam最低售价(换算前):{steamMinPrice}\t比例:{scale}".format(id=name,buffMinPrice=buffMinPrice,steamMinPrice=steamMinPrice,scale=scale))
          #赋值区
          try:
            sql="insert into buff values({id},'{name}',{buffMinPrice},{steamMinPrice},{scale},\
            {scaleSteam2Buff},{minus_steam2buff},{buffonSale},{buffBuy},'{type}',{buyMaxPrice},'{exterior}','{steamMarketLink}','{time}')".format\
            (id=id,name=name,buffMinPrice=buffMinPrice,steamMinPrice=steamMinPrice,scale=scale,scaleSteam2Buff=scaleSteam2Buff,
             minus_steam2buff=minus_steam2buff,buffonSale=buffonSale,buffBuy=buffBuy,type=type,buyMaxPrice=buyMaxPrice,exterior=exterior,
             steamMarketLink=steamMarketLink,time=nowString)
            print(sql)
            c.execute(sql)  # 执行sql语句
            conn.commit()  # 提交数据库操作
          except sqlite3.IntegrityError:
            sql="update buff set name='{name}',buff_min_price={buffMinPrice},steam_min_Price={steamMinPrice},\
            scale_steam2buff={scaleSteam2Buff},minus_steam2buff={minus_steam2buff},buffonSale={buffonSale},buffBuy={buffBuy},\
            type='{type}',buy_max_price={buyMaxPrice},exterior='{exterior}',steam_market_link='{steamMarketLink}',\
            time='{time}',scale_buff2steam={scale} where id={id}".format \
                (id=id, name=name, buffMinPrice=buffMinPrice, steamMinPrice=steamMinPrice, scale=scale,
                 scaleSteam2Buff=scaleSteam2Buff,
                 minus_steam2buff=minus_steam2buff, buffonSale=buffonSale, buffBuy=buffBuy, type=type,
                 buyMaxPrice=buyMaxPrice, exterior=exterior,
                 steamMarketLink=steamMarketLink, time=nowString)
            print(sql)
            c.execute(sql)  # 执行sql语句
            conn.commit()  # 提交数据库操作
          #键值错误处理，调试中



      return

def urlAnalyze(str):
  "URL解析，由大类页面分析该大类消息"
  url = ("https://buff.163.com/api/market/goods?game=csgo&page_num=1&category_group=%s&_=1607400865227") % str
  headers = {
      'Cookie': Cookies
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
        url = ("https://buff.163.com/api/market/goods?game=csgo&page_num={}&category_group={}&_=1607400865227".format(i,str))
        buck(url)
  else:
      print("-----------------------------------获取物品大类信息失败------------------------------------------------------")
      print(content)
      return


url= 'other'
urlAnalyze(url)
print(c.execute('select id from buff'))
