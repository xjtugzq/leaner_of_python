'''
获取知乎某问题下所有图片（抄的）
'''
from urllib import request
from bs4 import BeautifulSoup as bs
import re
import time
url = r'https://www.zhihu.com/question/22918070'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}
page = request.Request(url, headers=headers)
page_info = request.urlopen(page).read().decode('utf-8')
soup = bs(page_info, 'html.parser')
links = soup.find_all('img', 'origin_image zh-lightbox-thumb',src=re.compile(r'.jpg$'))
local_path = r'H:\code\Python\pic'

for link in links:
    request.urlretrieve(link.attrs['src'], local_path + r'\%s.jpg' % time.time())