# -*- coding: utf-8 -*-
import os
import requests
import re
import pandas as pd
import time
import random
import sys
reload(sys)
sys.setdefaultencoding('gbk')

def Save(save_path, filename, item):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path+"/"+filename+".csv"
    with open(path, "w+") as fp:
        #fp.write('datetime,insName,insStar,rate,secuFullCode,secuName,sys16, sys17, sys18,,,title')
        fp.write('test1,test2, test3, test4, test5, test6, test7 ,test8,test9,test10,test11,test12,test13,test14,test15,test16,test17,test18,test19')
        fp.write('\n')
        for i in item:
            for j in i:
                j = j.decode("gbk")
                fp.write(j)
                fp.write(',')
            fp.write('\n')
            
def Crawler(url):
    print "downloading", url
    myPage = requests.get(url).content.decode("utf8")
    #with open("eastmoney.txt", "w+") as fp:
        #fp.write(myPage.encode("utf8"))
    return myPage

def Page_Info(myPage):
    mypage_Info = re.findall()

print "start"
print "This is a crawler that extract data from http://data.eastmoney.com/bbsj/201512/yjbb.html"
save_path = u"eastmoney_nbyj"
year = raw_input("Give me the date(e.g. 2016-09-30): ")
filename = "nbyj_" + year
text = ""
num = int(raw_input("How many pages do you except the crawler to walk through? "))
for i in range(1, num + 1):
    url = u"http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SR&sty=YJBB&fd=" + year + "&st=13&sr=-1&p=" + str(i) + "&ps=50&js=var%20wMihohub={pages:(pc)"
    text = text + Crawler(url) + '\n'
    time.sleep(0 + random.randint(0, 2))
print "Finish downloading"
p = re.compile(u'"(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)"')
print "finding pattern"
item = p.findall(text)
print "saving"
Save(save_path, filename, item)
df = pd.read_csv(save_path+"/"+filename+".csv", dtype = str, encoding = 'gbk', index_col = False, sep = ',')
for i in range(len(df.index)):
    df.set_value(i, 'test1', '=' + '"' + df.values[i][0] + '"')
    
df.to_csv("eastmoney_nbyj/nbyj_" + year + ".csv", encoding = 'gbk', index = False)
print "end"
