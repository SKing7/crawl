#!/usr/env python
#coding:utf-8

import json
import net
import urllib
from BeautifulSoup import BeautifulSoup
import xlwt
import sys
import cgi
reload(sys)
sys.setdefaultencoding('utf-8')

#从字符串中提取出需要打印输出的内容
def extract_args(str, city, loc, cate):
    host = "http://www.yelp.com"
    htmlEncoding = '';
    data = []
    soup = BeautifulSoup(str, htmlEncoding);
    foundClass = soup.findAll(attrs={"class":"biz-name"});
    for found in foundClass:
        line = []
        line.append(loc)
        line.append(city)
        line.append(cate)
        if not found.string:
            name = '';
            for content in found.contents:
                try:
                    name += content.contents
                except:
                    name += content.string
            line.append(name)
        else:
            line.append(cgi.unescape(found.string))
        line.append(host + found['href'])
        data.append(line)
    return data

def outputfile(filename, data):
    file = xlwt.Workbook()
    table = file.add_sheet('sheet name')
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = 'Times New Roman'
    style.font = font
    line = [['province', 'city', 'category', 'bizname', 'url']]
    data = line + data
    i = 0
    for line in data:
        j = 0
        for item in line:
            if isinstance(item, unicode):
                table.write(i,j,item, style)
            else:
                try:
                    item = item.decode('gbk')
                    table.write(i,j,item.decode('gbk'), style)
                except:
                    table.write(i,j,item, style)
                    
            j += 1
        i += 1
    file.save(filename)


#查找关键字
find_desc = '';
#查找的地域
find_city = 'San Francisco';
find_loc = 'CA';
ns = 1;
file_name = 'test.xls'

if(len(sys.argv) < 4):
    print "Usage: "+sys.argv[0]+" 关键字 城市 地域  文件名"
    exit()
else:
    cflt = sys.argv[1]
    find_city = sys.argv[2]
    find_loc =  sys.argv[3]
    file_name = sys.argv[4]
    
start = 0
all_data = []
n = net.Net()
while True:
    find_place = find_city + "," + find_loc
    data = { 
        'ns':ns,
        'cflt':cflt,
        'start': start,
        'find_loc':find_place,
        'find_desc':find_desc,
    }
    url = 'http://www.yelp.com/search?'
    url += urllib.urlencode(data)
    str = n.get(url)
    args = extract_args(str, find_city, find_loc, cflt)
    count = len(args)
    if count == 0:
        break;
    all_data += args
    start += count
    print start
    #if start>9:
    #    break
outputfile(file_name, all_data)

