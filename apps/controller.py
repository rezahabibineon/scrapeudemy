from utils.utils import news_scraper

class NewsController(object):
    
    @classmethod
    def get_news(cls, num_news):
        data = news_scraper(num_news)
        return len(data), data