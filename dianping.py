#!/usr/env python
#coding:utf-8
from datetime import *
import json
import net
import urllib
from BeautifulSoup import BeautifulSoup
import sys
import os
import cgi
import re
import time
import urlparse
import mail
reload(sys)
sys.setdefaultencoding('utf-8')
n = net.Net()
url = 'http://www.dianping.com/card/'

#从字符串中提取出需要打印输出的内容
def extract_args(city, cate, str):
    soup = BeautifulSoup(str)
    #获取所有的页数
    pages = 1
    href = "?pageno=1&trigger=0&sort=1&desc=1&q=&joined=1";
    foundclass = soup.findAll(attrs={'onclick':re.compile("5_mc_cardlist_nextpage")})
    for found in foundclass:
        try:
            i = int(found['title'])
        except UnicodeEncodeError:
            i = 0
        if i>pages :
            pages = i
            href = found['href']
    #获取每一页的数量
    found = soup.findAll(attrs={'class':re.compile("li-hover card-")})
    numPerPage = len(found)
    #获取最后一页的数量
    time.sleep(2);
    data = n.get(url + city + cate + href)
    soup = BeautifulSoup(data)
    found = soup.findAll(attrs={'class':re.compile("li-hover card-")})
    lastPage = len(found)
    bizNum = int(numPerPage)*(int(pages)-1) + lastPage
    return bizNum

args = '?trigger=0&sort=1&desc=1&q=&joined=1'
categorys = {'/search/d0_c0':'全部', '/search/d0_c10':'美食'};
citys = {
        'shanghai':'上海',
        'beijing':'北京',
        'guangzhou':'广州',
        'shenzhen':'深圳',
        'tianjin':'天津',
        'xian':'西安',
        'fuzhou':'福州',
        'chongqing':'重庆',
        'hangzhou':'杭州',
        'ningbo':'宁波',
        'wuxi':'无锡',
        'nanjing':'南宁',
        'hefei':'合肥',
        'wuhan':'武汉',
        'chengdu':'成都',
        'qingdao':'青岛',
        'xiamen':'厦门',
        'dalian':'大连',
        'shenyang':'沈阳',
        'changsha':'长沙',
        'zhengzhou':'郑州',
        'suzhou':'苏州',
        'jinan':'济南',
        'haerbin':'哈尔滨',
        }
data = []
for city,cityname in citys.items():
    n.get(url+city)
    time.sleep(5)
    for cate,catename in categorys.items():
        str = n.get(url + city + cate + args)
        nums = extract_args(city, cate, str)
        print "%s\t%s\t%d" %(cityname,catename,nums)
        data.append((cityname, catename, nums))
        time.sleep(3)
#将获取到的数据通过邮件发送出去
content = '<table id="standard-table" border="1"><tr><th>日期</th><th>城市</th><th>品类</th><th>数量</th></tr>'
for line in data:
    content += '<tr><td>%s</td>' %date.today()
    content += '<td>%s</td><td>%s</td><td>%s</td></tr>' %line
content += '</table>'
mail.send_mail("lishipeng@meituan.com","","点评数据抓取", content)


