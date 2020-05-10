import requests
from bs4 import BeautifulSoup

def getText(baseurl,sectionurl):
    page_req = requests.get(baseurl+sectionurl)
    html = page_req.text.encode('iso-8859-1')
    bf = BeautifulSoup( html)
    titles = bf.find_all('div', id='nr_title')
    texts = bf.find_all('div', id='nr1')
    title = titles[0].string
    text = texts[0].text
    nexturl = bf.find_all('a',id = 'pb_next')[0].get('href').split('/')[-1]
    fo = open('xn.txt', "ab+")
    fo.write(('\r' + title + '\r\n').encode('UTF-8'))
    fo.write((text).encode('UTF-8'))
    fo.close()
    return nexturl
baseurl = 'https://m.37zw.net/2/2197/'
sectionurl = '819673.html'
while (sectionurl != ''):
    sectionurl = getText(baseurl, sectionurl)
