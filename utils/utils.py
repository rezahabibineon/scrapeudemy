from ast import Num
import time
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

def news_scraper(q=None):
    homepage_news = get_homepage()
    data = []

    len_news = len(homepage_news)
    
    if q and q<len_news:
        len_news = q

    for n in range(len_news+1):
        if "live" in homepage_news[n].find('a')['href']:  
            continue
        
        link = homepage_news[n].find('a')['href']    
        title = homepage_news[n].find('a').get_text()
        
        article_resp = requests.get(link)
        article_content = article_resp.content
        
        soup_article = BeautifulSoup(article_content, 'html5lib')
        body_article = soup_article.find_all('div', class_='article-body-commercial-selector article-body-viewer-selector dcr-ucgxn1')
        
        full_paragraph = body_article[0].find_all('p')
        list_paragraph = []

        for p in range(0, len(full_paragraph)):
            paragraph = full_paragraph[p].get_text()
            list_paragraph.append(paragraph)
            content = " ".join(list_paragraph)
            
        data.append({
            "link": link,
            "title": title,
            "content": content,
        })

    return data