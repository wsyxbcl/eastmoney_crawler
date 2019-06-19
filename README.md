# eastmoney_crawler  
Crawler that walks through the “业绩报告” and the “年报业绩” part of the data.eastmoney.com  
Just a simple script, antidup version avoids getting duplicated stock, which means only the latest data of one stock will be downloaded.  
<del> Python 2.7 is used for this is based on one of my old test code and I don't think such simple code worth an update. </del>

Now it is revised to Python 3.x version, where the antiduplicate function is also integrated in the eastmoney_yjbg.py. The old Python 2.7 version is still available in the python2 branch.
