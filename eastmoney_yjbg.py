import os
import requests
import re
import time
import random
import sys
from pathlib import Path

import pandas as pd

from eastmoney_nbyj import save_report, report_crawler


def anti_duplicate(frame):
    '''
    Used to delete the duplicated case in dateframe
    '''
    frame = frame.drop_duplicates(['secuFullCode'])
    return frame


if __name__ == '__main__':
    print("Start")
    print("This is a crawler that extract data from http://data.eastmoney.com/report/")
    num = int(input("How many pages do you except the crawler to walk through? "))
    save_path = "eastmoney_yjbg"
    filename = "eastmoney_yjbg.csv"
    # url_file = open("url.txt")
    # line = url_file.readline()
    text = ""
    for i in range(1, num + 1):
        url = "http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&js=var%20lnamgZzE={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&ps=50&p="+str(i)
        text = text+report_crawler(url)+'\n'
        time.sleep(0 + random.randint(0,2))
        #line = url_file.readline()
    # url_file.close()
    # text = Crawler(url_1).encode("gbk")+Crawler(url_2).encode("gbk")+Crawler(url_3).encode("gbk")+Crawler(url_4).encode("gbk")+Crawler(url_5).encode("gbk")+Crawler(url_6).encode("gbk")+Crawler(url_7).encode("gbk")+Crawler(url_8).encode("gbk")+Crawler(url_9).encode("gbk")+Crawler(url_10).encode("gbk")+Crawler(url_11).encode("gbk")+Crawler(url_12).encode("gbk")
    #p = re.compile('"change":"(.*?)","companyCode":"(.*?)","datetime":"(.*?)","infoCode":"(.*?)","insCode":"(.*?)","insName":"(.*?)","insStar":"(.*?)","jlrs":\["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\],"rate":"(.*?)","secuFullCode":"(.*?)","secuName":"(.*?)","sratingName":"(.*?)","sy":"(.*?)","syls":\["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\],"sys":\["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\],"title":"(.*?)","profitYear":"(.*?)","type":"(.*?)","newPrice":"(.*?)"},')
    p = re.compile('"datetime":"(.*?)",.*?"insName":"(.*?)","insStar":"(.*?)",.*?"rate":"(.*?)","secuFullCode":"(.*?)","secuName":"(.*?)",.*?"sys":\["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\],"title":"(.*?)",')
    item = p.findall(text)
    save_report(save_path, filename, item,
                head='datetime,insName,insStar,rate,secuFullCode,secuName,sys16,sys17,sys18,,,title')
    #df = pd.read_csv(save_path+"/"+filename+".csv", encoding = 'gbk', index_col = False)
    df = pd.read_csv(Path(save_path).joinpath(filename), index_col=False, sep=',', error_bad_lines=False)

    cols = list(df)
    cols.insert(0, cols.pop(cols.index('secuName')))
    df = df.ix[:, cols]
    cols.insert(0, cols.pop(cols.index('secuFullCode')))
    df = df.ix[:, cols]

    for i in range(len(df.index)):
        df.at[i, 'secuFullCode'] = ('='+'"'+str(df.values[i][0][0:6])+'"')
    # for i in df.values:
        # new_df.append(i[0][0:6])
    # df[0] = new_df

    df.to_csv(Path(save_path).joinpath('eastmoney_yjbg_revised.csv'), index=False)

    df = anti_duplicate(df)
    df.to_csv(Path(save_path).joinpath('eastmoney_yjbg_antidup.csv'), index=False)
    print("end")