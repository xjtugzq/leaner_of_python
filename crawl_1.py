'''

获取简书首页文章标题（抄的）

'''

from urllib import request

from bs4 import BeautifulSoup as bs

url = r'http://www.jianshu.com'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}

page = request.Request(url, headers=headers)

page_info = request.urlopen(page).read().decode('utf-8')

soup = bs(page_info, 'html.parser')

titles = soup.find_all('a', 'title')

#for title in titles:

#    print(title.string)

try:

    file = open(r'H:\code\Python\title.txt', 'w')

    for title in titles:

        file.write(title.string + '\n')

finally:

    if file:

        file.close()
