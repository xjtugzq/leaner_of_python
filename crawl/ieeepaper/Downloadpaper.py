import requests
import pandas as pd
from headers import headers_pdf
import time
import numpy as np
import re


results = pd.read_csv('records.csv', encoding='gbk') 
n = len(results['link'])
for index in range(0, n):
    try:
        rstr = r"[\/\\\:\*\?\"\<\>\|]"
        title = re.sub(rstr, "_", results['title'][index])
        filename = str(results['publicationYear'][index]) + '-' + title + '.pdf'
        path = 'H:/code/Python/DownloadPaper/paper/'
        resource = requests.get(results['pdf_link'][index], headers=headers_pdf)
        with open(path + filename, mode="wb") as fh:
            fh.write(resource.content)
        fh.close()
        sleepTime = np.random.randint(5, 10)
        time.sleep(sleepTime)
        print("第%s篇下载完成" % (index + 1))
    except Exception as e:
        failedtimes = failedtimes + 1
        f = open('logging.txt', 'a')
        now = time.strftime("%Y/%m/%d/%H:%M:%S", time.localtime())
        f.write(now)
        f.write(' ' + "下载第%s篇pdf时出错：" % str(index + 1))
        f.write(repr(e))
        f.write('\n')
        f.close()
        #print("第%s篇下载失败" % (index+1))
