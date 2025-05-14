#!/usr/bin/python3
import datetime
import os
import requests
import re
import time
import random
import sys
from pathlib import Path

import pandas as pd

from eastmoney_nbyj import report_crawler

base_url = "http://reportapi.eastmoney.com/report/list?pageSize=100&beginTime=2010-10-08&endTime={}&pageNo={}&qType=0"

def anti_duplicate(df):
    df['publishDate'] = pd.to_datetime(df['publishDate'], errors='coerce')

    # Drop rows where all three prediction columns are NaN
    df = df.dropna(subset=['predictNextTwoYearEps', 'predictNextYearEps', 'predictThisYearEps'], how='all')

    def get_priority(row):
        if pd.notna(row['predictNextTwoYearEps']):
            return 3
        elif pd.notna(row['predictNextYearEps']):
            return 2
        elif pd.notna(row['predictThisYearEps']):
            return 1
        else:
            return 0

    df['priority'] = df.apply(get_priority, axis=1)

    df = df.sort_values(by=['stockName', 'priority', 'publishDate'], ascending=[True, False, False])

    df = df.drop_duplicates(subset='stockName', keep='first')

    df = df.drop(columns='priority')

    return df


if __name__ == '__main__':
    print("Start crawling")
    date_today = datetime.datetime.today().strftime('%Y-%m-%d')
    print("Extracting data from http://data.eastmoney.com/report, date:{}".format(date_today))
    num_pages = int(input("Number of pages to crawl (100 entrances per page): "))
    save_path = "eastmoney_yjbg"
    filename = "eastmoney_yjbg_{}_raw.csv".format(date_today)

    reports = []
    print("Crawling")
    for page_num in range(1, num_pages + 1):
        url = base_url.format(date_today, page_num)
        print(f"{page_num} of {num_pages} pages")
        reports += report_crawler(url)['data']
        time.sleep(0 + random.randint(0, 2))
    
    df = pd.DataFrame(reports)
    df.to_excel(Path(save_path).joinpath('eastmoney_yjbg_{}_原始数据.xlsx'.format(date_today)), index=False)

    print("\nRemoving duplicated entries")
    df = anti_duplicate(df)
    df.to_excel(Path(save_path).joinpath('eastmoney_yjbg_{}_去重数据.xlsx'.format(date_today)), index=False)
    print("Anti_dup file saved")