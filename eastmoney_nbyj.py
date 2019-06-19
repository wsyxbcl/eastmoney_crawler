import os
import requests
import re
import time
import random
import sys
from pathlib import Path

import pandas as pd

def save_report(save_path, filename, item):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = Path(save_path).joinpath(filename)
    with open(path, "w+") as fp:
        #fp.write('datetime,insName,insStar,rate,secuFullCode,secuName,sys16, sys17, sys18,,,title')
        fp.write('test1, test2, test3, test4, test5, test6, test7 ,test8,test9,test10,test11,test12,test13,test14,test15,test16,test17,test18,test19')
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
    #with open("eastmoney.txt", "w+") as fp:
        #fp.write(myPage.encode("utf8"))
    return myPage

if __name__ == '__main__':
    print("start")
    print("This is a crawler that extracts data from http://data.eastmoney.com/bbsj/201512/yjbb.html")
    save_path = "eastmoney_nbyj"
    year = input("Give me the date(e.g. 2016-09-30): ")
    filename = "nbyj_"+year+'.csv'
    text = ""
    num = int(input("How many pages do you except the crawler to walk through? "))
    for i in range(1, num + 1):
        url = "http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SR&sty=YJBB&fd=" + year + "&st=13&sr=-1&p=" + str(i) + "&ps=50&js=var%20wMihohub={pages:(pc)"
        text = text+report_crawler(url)+'\n'
        time.sleep(0 + random.randint(0, 2))
    print("Finish downloading")
    p = re.compile('"(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)"')
    print("Finding pattern")
    item = p.findall(text)
    print("Saving to"+str(Path(save_path).joinpath(filename)))
    save_report(save_path, filename, item)
    df = pd.read_csv(Path(save_path).joinpath(filename), dtype=str, index_col=False, sep=',')

    for i in range(len(df.index)):
        # df.set_value(i, 'test1', '='+'"'+df.values[i][0]+'"') # for excel
        df.at[i, 'test1'] = ('='+'"'+df.values[i][0]+'"') # for excel
        
    df.to_csv("eastmoney_nbyj/nbyj_"+year+".csv", index=False)
    print("Bye")
