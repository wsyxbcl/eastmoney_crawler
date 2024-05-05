import json
import os
import requests
import re
import time
import random
import sys
from pathlib import Path

import pandas as pd

base_url = "https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=UPDATE_DATE,SECURITY_CODE&sortTypes=-1,-1&pageSize={page_size}&pageNumber={page_num}&reportName=RPT_LICO_FN_CPD&columns=ALL&filter=(REPORTDATE=%27{up_to_date}%27)"

def report_crawler(url):
    reports = requests.get(url).content.decode("utf8")
    # p = re.compile("jQuery.*?\((.*?)\);$")
    # reports_json = json.loads(p.findall(reports)[0])
    reports_json = json.loads(reports)
    return reports_json

if __name__ == '__main__':
    print("Annual report data crawler from https://data.eastmoney.com/bbsj")
    save_path = "eastmoney_nbyj"
    date = input("The date (you can check the website, e.g. 2016-09-30): ")
    filename = "nbyj_"+date+'.csv'

    reports = []
    first_page = report_crawler(base_url.format(page_size='500', page_num='1', up_to_date=date))
    num_pages = first_page['result']['pages']
    reports += first_page['result']['data']

    for i in range(2, num_pages + 1):
        reports_json = report_crawler(base_url.format(page_size='500', page_num=str(i), up_to_date=date))
        reports += reports_json['result']['data']
        print("Crawling {} of {} pages...".format(i, num_pages))
        time.sleep(0 + random.randint(0, 2))

    print("Data downloaded, total pages: ", num_pages)
    df = pd.DataFrame(reports)
    # for worksheet softwares
    df['SECURITY_CODE'] = df['SECURITY_CODE'].map(lambda x: '="{}"'.format(x))
    print("Saving to "+str(Path(save_path).joinpath(filename)))
    df.to_csv(Path(save_path).joinpath('nbyj_'+date+'.csv'), encoding="utf_8_sig", index=False)
