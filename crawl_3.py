'''

获取陕师大招聘网所有企业名称和展位

'''

from urllib import request

from bs4 import BeautifulSoup as bs

import requests

import json





url = r'http://job.snnu.edu.cn/enterprise/auth/recruit/exhibitor'

headers = {

    'Accept': '*/*',

    'Connection': 'keep-alive',

    'Content-Length': '66',

    'Content-Type': 'application/json',

    'Cookie': 'JSESSIONID=42F9775C5CB698601865FEB585647BAB',

    'Host': 'job.snnu.edu.cn',

    'Content-Type':'application/json',

    'Origin': 'http://job.snnu.edu.cn',

    'Refer': 'http://job.snnu.edu.cn/web/student/employment/largeFair/fairDetail?id=621355599519387806',

    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',

    'X-Authorization':'Bearer'}

page_index = 1

size = 480

data = {"companyName":"","industry":"","nature":"","fairId":"621355599519387806","applyStatus":2,"page":page_index,"size":size}

data = json.dumps(data)

page = requests.post(url, data=data, headers=headers)



page_write = page.content.decode('utf-8')

results = json.loads(page_write)['data']['content']

#companyList = {'companyName': [], 'boothNumber': []}

try:

    file = open(r'H:\code\Python\comp.txt', 'w')

    file.write('companyName' + '\t' + 'bootNumber' + '\t' + 'address' + '\t' + 'city' + '\t' + 'companyId' + '\n')

    for result in results:

        file.write(result['companyName'] + '\t' + result['boothNumber'] + '\t' + str(result['address']) + '\t' + str(result['city']) + '\t' + str(result['companyId']) + '\n')

        #companyList['companyName'].append(result['companyName'])

        #companyList['boothNumber'].append(result['boothNumber'])

finally:

    if file:

        file.close()
