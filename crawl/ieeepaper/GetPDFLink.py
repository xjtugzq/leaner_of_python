import requests
import json
import time
from headers import headers, headers_link
import csv
from lxml import etree

'''
还存在一些问题，如每次下载不能超过50条，如果超过50条，则需要再等待半小时
我是以我们学校的账户登录的，其他账户不清楚
'''

searchKeys = '自己定义'    # 检索关键词
timeRange = [2010, 2019]  # 年份范围
refer_link = ('https://ieeexplore.ieee.org/search/searchresult.jsp?queryText='
              '%s&highlight=true&returnType=SEARCH&ranges=%d_%d_Year&returnFa'
              'ets=ALL&rowsPerPage=100' % (searchKeys.replace(' ', '%20'), timeRange[0], timeRange[1]))
headers['refer'] = refer_link
url = r'https://ieeexplore.ieee.org/rest/search'
pageNumber = 5
infoKey = ['authors', 'articleTitle', 'pdfLink', 'publicationYear', 'documentLink']


def getName(name_list):
    temp = []
    for name in name_list:
        if name != 'None':
            temp.append(name['preferredName'])
        else:
            temp = temp.append(['None'])
    return temp


def get_paper_info(url, headers, pageNumber):
    url0 = 'https://ieeexplore.ieee.org'
    results = {}
    for key in infoKey:
        results[key] = []
    for i in range(pageNumber):
        print("开始下载第%d页" % (i+1))
        data = {'highlight': 'true',
                'queryText': searchKeys,
                'ranges': ["%d_%d_Year" % (timeRange[0], timeRange[1])],
                '0': "%d_%d_Year" % (timeRange[0], timeRange[1]),
                'returnFacets': ["ALL"],
                '0': "ALL",
                'returnType': "SEARCH",
                'pageNumber': i + 1,
                'rowsPerPage': 100}
        data = json.dumps(data)
        page = requests.post(url, data=data, headers=headers)
        page_write = json.loads(page.content.decode('utf-8'))
        records = page_write['records']
        for record in records:
            for key in infoKey:
                try:
                    results[key].append(record[key])
                except KeyError:
                    results[key].append(['None'])
        print("第%s页下载完成" % (i + 1))
    authors = []
    for names in results['authors']:
        authors.append(getName(names))
    results['authors'] = authors
    time.sleep(10)
    return results


def getpdflink(results):
    failedtimes = 0
    results['pdf_link'] = results['link']
    for index in range(len(results['link'])):
        try:
            resource = requests.get(results['link'][index], headers=headers_link)
            html = etree.HTML(str(resource.content))
            xpath = '/html/body/iframe//@src'
            temp = html.xpath(xpath)
            results['pdf_link'][index] = temp[0].split('?')[0]
            print("第%d条获取成功" % (index + 1))
            time.sleep(2)
            failedtimes = 0
        except Exception as e:
            failedtimes = failedtimes + 1
            f = open('logging.txt', 'a')
            now = time.strftime("%Y/%m/%d/%H:%M:%S", time.localtime())
            f.write(now)
            f.write(' ' + "获取第%s条pdf_link出错：" % str(index + 1))
            f.write(repr(e))
            f.write('\n')
            f.close()
            #print("第%d条获取失败" % (index + 1))
        if failedtimes == 5: #连续失败表示访问受限
            break
    return results


def writeinfo(results):
    with open('records.csv', 'w') as f:
        infoKeynew = infoKey
        infoKeynew.append('pdf_link')
        writer = csv.DictWriter(f, fieldnames=infoKeynew, lineterminator='\n')
        writer.writeheader()
        for index in range(len(results['title'])):
            try:
                writer.writerow({key: results[infoKeynew][index] for key in infoKeynew})
            except Exception as e:
                f = open('logging.txt', 'a')
                now = time.strftime("%Y/%m/%d/%H:%M:%S", time.localtime())
                f.write(now)
                f.write(' ' + "写入第%s条信息出错：" % str(index + 1))
                f.write(repr(e))
                f.write('\n')
                f.close()
                #print("第%s行输出出现错误" % (index + 1))
    f.close()
    return ''


if __name__ == '__main__':
    results = get_paper_info(url, headers, pageNumber)
    results = getpdflink(results)
    writeinfo(results)


