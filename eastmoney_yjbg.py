import datetime
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
    Delete duplicated cases in dataframe
    '''
    frame = frame.drop_duplicates(['secuFullCode'])
    return frame


if __name__ == '__main__':
    print("Crawling Started")
    date_today = datetime.datetime.today().strftime('%Y-%m-%d')
    print("Extracting data from http://data.eastmoney.com/report, date:{}".format(date_today))
    num_pages = int(input("Number of pages to walk through (100 entrances per page): "))
    save_path = "eastmoney_yjbg"
    filename = "eastmoney_yjbg_{}_raw.csv".format(date_today)

    text = ""
    for page_num in range(1, num_pages + 1):
        # url = "http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&js=var%20lnamgZzE={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&ps=50&p="+str(i)
        url = "http://reportapi.eastmoney.com/report/list?pageSize=100&beginTime=2010-10-08&endTime={}&pageNo={}&qType=0".format(date_today, page_num)
        text = text+report_crawler(url)+'\n'
        time.sleep(0 + random.randint(0, 2))
    
    p = re.compile('"title":"(.*?)",.*?'
                    '"stockName":"(.*?)",.*?'
                    '"stockCode":"(.*?)",.*?'
                    '"publishDate":"(.*?)",.*?'
                    '"predictNextTwoYearEps":"(.*?)",.*?'
                    '"predictNextTwoYearPe":"(.*?)",.*?'
                    '"predictNextYearEps":"(.*?)",.*?'
                    '"predictNextYearPe":"(.*?)",.*?'
                    '"predictThisYearEps":"(.*?)",.*?'
                    '"predictThisYearPe":"(.*?)",.*?'
                    '"indvInduName":"(.*?)",.*?'
                    '"emRatingName":"(.*?)",.*?'
                    '"sRatingName":"(.*?)",.*?')
    # p = re.compile('"datetime":"(.*?)",.*?"insName":"(.*?)","insStar":"(.*?)",.*?"rate":"(.*?)","secuFullCode":"(.*?)","secuName":"(.*?)",.*?"sys":\["(.*?)","(.*?)","(.*?)","(.*?)","(.*?)"\],"title":"(.*?)",')
    item = p.findall(text)
    save_report(save_path, filename, item,
                head=("title, stockName, stockCode, publishDate, "
                      "predictNextTwoYearEps, predictNextTwoYearPe, "
                      "predictNextYearEps, predictNextYearPe, "
                      "predictThisYearEps, predictThisYearPe, "
                      "indvInduName, emRatingName, sRatingName")
    df = pd.read_csv(Path(save_path).joinpath(filename), index_col=False, sep=',', error_bad_lines=False)

    cols = list(df)
    cols.insert(0, cols.pop(cols.index('stockName')))
    cols.insert(0, cols.pop(cols.index('stockCode')))
    df = df.ix[:, cols]

    for i in range(len(df.index)):
        df.at[i, 'stockCode'] = ('='+'"'+str(df.values[i][0][0:6])+'"')

    df.to_csv(Path(save_path).joinpath('eastmoney_yjbg_{}_revised.csv'.format(date_today)), index=False)

    df = anti_duplicate(df)
    df.to_csv(Path(save_path).joinpath('eastmoney_yjbg_{}_antidup.csv'.format(date_today)), index=False)
    print("end")