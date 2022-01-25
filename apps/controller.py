from utils.utils import get_news

class NewsController(object):
    
    @classmethod
    def get_news(cls, num_news):
        data = get_news(num_news)
        return len(data), data