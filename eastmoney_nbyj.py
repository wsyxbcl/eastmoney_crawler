import os
import requests
import re
import time
import random
import sys
from pathlib import Path

import pandas as pd

base_url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SR&sty=YJBB&fd={date}&st=13&sr=-1&p={page}"

def save_report(save_path, filename, item, head):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = Path(save_path).joinpath(filename)
    with open(path, "w+") as fp:
        fp.write(head)
        fp.write('\n')
        for i in item:
            for j in i:
                if ',' in j:
                    j = j.replace(',', '')                        
                try:
                    fp.write(j)
                except UnicodeEncodeError as e:
                    print('***************')
                    print("Expected error:")
                    print(e)
                    print(j)
                    print("The error is ignored")
                    print()
                    continue
                fp.write(',')
            fp.write('\n')
            
def report_crawler(url):
    print("downloading "+url)
    myPage = requests.get(url).content.decode("utf8")
    return myPage

if __name__ == '__main__':
    base_url
    print("start")
    print("This crawler downloads annual report data from https://data.eastmoney.com/bbsj")
    save_path = "eastmoney_nbyj"
    date = input("Give me the date(e.g. 2016-09-30): ")
    filename = "nbyj_"+date+'.csv'
    text = ""
    num = int(input("How many pages do you expect to walk through? "))
    for i in range(1, num + 1):
        url = base_url.format(date=date, page=str(i))
        text += report_crawler(url)+'\n'
        time.sleep(0 + random.randint(0, 2))
    print("Download finished")
    p = re.compile('"(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)"')
    print("Finding patterns")
    item = p.findall(text)
    print("Saving to "+str(Path(save_path).joinpath(filename)))
    save_report(save_path, filename, item, 
                head='col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11,col12,col13,col14,col15,col16,col17,col18,col19')
    df = pd.read_csv(Path(save_path).joinpath(filename), dtype=str, index_col=False, sep=',')

    for i in range(len(df.index)):
        # df.set_value(i, 'col1', '='+'"'+df.values[i][0]+'"') # for excel
        df.at[i, 'col1'] = ('='+'"'+df.values[i][0]+'"') # for excel
        
    df.to_csv(Path(save_path).joinpath('nbyj_'+date+'.csv'), index=False)
    print("Bye")
