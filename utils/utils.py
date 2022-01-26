import re
import time
import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_homepage():
    #url 
    url = "https://www.theguardian.com/uk"

    homepage_resp = requests.get(url)
    homepage_resp.status_code

    homepage_content = homepage_resp.content
    homepage_soup = BeautifulSoup(homepage_content, 'html5lib')

    homepage_news = homepage_soup.find_all('h3', class_='fc-item__title')
    #len(homepage_news)

    return homepage_news

def get_content(body_article, attr=None):
    try:
        content = ''
        
        list_paragraph = []
        full_paragraph = body_article[0].find_all('p')
        for p in range(0, len(full_paragraph)):
            paragraph = full_paragraph[p].get_text()
            list_paragraph.append(paragraph)
            content = " ".join(list_paragraph)

        return content    

    except:
        return 'contain image or video content'

def get_date(soup_article, attr=None):
        date = datetime.date.today().strftime("%A %d %b %Y")

        # if soup_article.find('time', class_='content__dateline-wpd js-wpd'):
        #     date = soup_article.find('time', class_='content__dateline-wpd js-wpd').get_text()
            
        date_token = ['dcr-hn0k3p', ' dcr-hn0k3p', 'dcr-km9fgb', ' dcr-km9fgb']
        for dt in date_token:
            if soup_article.find('label', class_=dt):
                date = soup_article.find('label', class_=dt).get_text()
            elif soup_article.find('div', class_=dt):
                date = soup_article.find('div', class_=dt).get_text()

        return " ".join(map(str, date.split(' ')[1:4]))

def get_title(soup_article, attr=None):
    txt = soup_article.find('a')['href']
    txt = txt.split('/')[-1].replace('-', ' ').title()
    return txt

def get_author(soup_article, attr=None):
    author = 'NA'

    author_token = ['dcr-igntr1', ' dcr-igntr1', 'dcr-ponjtt', '  dcr-ponjtt', 'dcr-wj7ien', 
                    ' dcr-wj7ien', 'dcr-x4zvo6', ' dcr-x4zvo6', 'dcr-x6uqxm', ' dcr-x6uqxm', 
                    'dcr-1c8zp3f', ' dcr-1c8zp3f', 'dcr-1g3eqzh', ' dcr-1g3eqzh', 'dcr-1mp5s8u', 
                    ' dcr-1mp5s8u','dcr-187adts', ' dcr-187adts', 'dcr-15zwths', ' dcr-15zwths']
    for at in author_token:
        if soup_article.find('div', class_=at):
            if soup_article.find('div', class_=at).find('a'):
                author = soup_article.find('div', class_=at).find('a').get_text()
            else:
                author = soup_article.find('div', class_=at).get_text() 
        elif soup_article.find('span', class_=at):
            if soup_article.find('span', class_=at).find('a'):
                author = soup_article.find('span', class_=at).find('a').get_text()
            else:
                author = soup_article.find('span', class_=at).get_text()
        elif soup_article.find('p', class_='byline'):
            author = soup_article.find('p', class_='byline').get_text()        

    return author        

def get_medsoc(soup_article, attr=None):
        medsoc = 'NA'
        
        medsoc_token = ['dcr-mjksz5', ' dcr-mjksz5']
        for mt in medsoc_token:
            if soup_article.find('div', class_=mt) and soup_article.find('div', class_=mt).find('a'):
                medsoc = soup_article.find('div', class_=mt).find('a').get_text()
            elif attr and  attr != 'NA':
                ms = re.sub("[^0-9a-zA-Z]+", "", attr.lower().replace(' ', ''))
                medsoc = '@' + ms

        return medsoc

def get_news(q=None):
    homepage_news = get_homepage()
    data = []

    len_news = len(homepage_news)
    
    if q and q<len_news:
        len_news = q

    for n in range(len_news):
        if "live" in homepage_news[n].find('a')['href']:
            continue
        
        link = homepage_news[n].find('a')['href']    
        title = get_title(homepage_news[n])
        
        article_resp = requests.get(link)
        article_content = article_resp.content
        
        soup_article = BeautifulSoup(article_content, 'html5lib')
        body_article = soup_article.find_all('div', class_='article-body-commercial-selector article-body-viewer-selector dcr-ucgxn1')
        
        date = get_date(soup_article)
        author = get_author(soup_article, None)
        medsoc = get_medsoc(soup_article, author)
        content = get_content(body_article)
        category = link.split('/')[3]
        len_title = len(title.split(' '))
        len_content = len(content.split(' '))
          
        data.append({
            "date": date,
            "author": author,
            "medsoc": medsoc,
            "link": link,
            "title": title,
            "content": content,
            "category": category,
            "len_title": len_title,
            "len_content": len_content,
        })

    return data