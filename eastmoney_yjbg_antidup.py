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
    '''
    write item to <filename>.csv and save to <save_path>
    '''
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path+"/"+filename+".csv"
    with open(path, "w+") as fp:
        fp.write('datetime,insName,insStar,rate,secuFullCode,secuName,sys16, sys17, sys18,,,title')
        fp.write('\n')
        for i in item:
            for j in i:
                try:
                    fp.write(j)
                except UnicodeEncodeError:
                    print "a gbk decoding error occurs"
                    print j
                    print "The error is ignored"
                    continue
                fp.write(',')
            fp.write('\n')
            
def Crawler(url):
    '''
    download given url
    '''
    print "downloading", url
    myPage = requests.get(url).content.decode("utf8")
    #with open("eastmoney.txt", "w+") as fp:
        #fp.write(myPage.encode("utf8"))
    return myPage
        
# def Page_Info(myPage):
    # mypage_Info = re.findall()

def Anti_duplicate(frame):
    '''
    Used to delete the duplicated case in dateframe
    '''
    frame = frame.drop_duplicates(['secuFullCode'])
    return frame

print "Start"
print "This is a crawler that extract data from http://data.eastmoney.com/report/"
num = int(raw_input("How many pages do you except the crawler to walk through? "))
save_path = u"eastmoney_yjbg"
filename = u"eastmoney_yjbg_antidup"
# url_file = open("url.txt")
# line = url_file.readline()
text = ""
for i in range(1, num + 1):
    url = u"http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&js=var%20lnamgZzE={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&ps=50&p=" + str(i)
    text = text + Crawler(url) + '\n'
    time.sleep(0 + random.randint(0,2))
    #line = url_file.readline()
# url_file.close()
# text = Crawler(url_1).encode("gbk")+Crawler(url_2).encode("gbk")+Crawler(url_3).encode("gbk")+Crawler(url_4).encode("gbk")+Crawler(url_5).encode("gbk")+Crawler(url_6).encode("gbk")+Crawler(url_7).encode("gbk")+Crawler(url_8).encode("gbk")+Crawler(url_9).encode("gbk")+Crawler(url_10).encode("gbk")+Crawler(url_11).encode("gbk")+Crawler(url_12).encode("gbk")
#p = re.compile('"change":"(.*?)","companyCode":"(.*?)","datetime":"(.*?)","infoCode":"(.*?)","insCode":"(.*?)","insName":"(.*?)","insStar":"(.*?)","jlrs":\["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\],"rate":"(.*?)","secuFullCode":"(.*?)","secuName":"(.*?)","sratingName":"(.*?)","sy":"(.*?)","syls":\["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\],"sys":\["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\],"title":"(.*?)","profitYear":"(.*?)","type":"(.*?)","newPrice":"(.*?)"},')
p = re.compile('"datetime":"(.*?)",.*?"insName":"(.*?)","insStar":"(.*?)",.*?"rate":"(.*?)","secuFullCode":"(.*?)","secuName":"(.*?)",.*?"sys":\["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\],"title":"(.*?)",')
item = p.findall(text)
Save(save_path, filename, item)
#df = pd.read_csv(save_path+"/"+filename+".csv", encoding = 'gbk', index_col = False)
df = pd.read_csv(save_path+"/"+filename+".csv", encoding = 'gbk', index_col = False, sep = ',', error_bad_lines=False)

cols = list(df)
cols.insert(0, cols.pop(cols.index('secuName')))
df = df.ix[:, cols]
cols.insert(0, cols.pop(cols.index('secuFullCode')))
df = df.ix[:, cols]

for i in range(len(df.index)):
    df.set_value(i, 'secuFullCode', '=' + '"' + str(df.values[i][0][0:6]) + '"')
# for i in df.values:
    # new_df.append(i[0][0:6])
# df[0] = new_df
df = Anti_duplicate(df)


df.to_csv("eastmoney_yjbg/eastmoney_yjbg_antidup.csv", encoding = 'gbk', index = False)
print "end"