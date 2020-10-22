from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
import pandas as pd
import nltk
from datetime import datetime
import yfinance as yf
import json


class DataCollector:

    def __init__(self, ticker, keywords_list, start_time, end_time):
        
        # configure for news downloading agent
        nltk.download('punkt')
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        self.config = Config()
        self.config.browser_user_agent = user_agent
        
        self.ticker = ticker
        self.price_df = None
        self.keywords_dict = None
        self.start_time = start_time
        self.end_time = end_time
        self.news_df = None
        self.link_filter_list = ['seekingalpha']
        # read the news searching JSON file
        with open('keywords.json', 'r') as fobj:
            self.keywords_dict = json.load(fobj)
        if not self.ticker in list(self.keywords_dict.keys()):
            raise ValueError('Ticker {:s} not supported!'.format(self.ticker))

    @staticmethod
    def gnews_date_fmt(date_in):
        return datetime.strftime(datetime.strptime(date_in, '%Y-%m-%d'), 
                                 '%m/%d/%Y')

    def search_news(self, max_page=10):
        news_list = list()
        # iterate for keywords
        for keyword in self.keywords_dict[self.ticker]:
            # GoogleNews accepcts different date format from yfinance
            googlenews_client = GoogleNews(start=self.gnews_date_fmt(self.start_time),
                                           end=self.gnews_date_fmt(self.end_time))
            googlenews_client.search(keyword)
            for i in range(1, max_page):
                googlenews_client.getpage(i)
            news_list = news_list + googlenews_client.result()
        # convert to pandas dataframe and remove duplicates
        temp_df = pd.DataFrame(news_list)
        temp_df.drop_duplicates(subset='link', inplace=True, keep='first')
        # get text from links
        content_list = list()
        for ind in temp_df.index:
            article_link = temp_df['link'][ind]
            if any(link_filter in article_link 
                    for link_filter in self.link_filter_list):
                continue
            try:
                record_dict = dict()
                article = Article(article_link, config=self.config)
                article.download()
                article.parse()
                record_dict = { 'Date': temp_df['date'][ind],
                                'Media': temp_df['media'][ind],
                                'Title':article.title,
                                'Article': article.text,
                                'Link': article_link }
                content_list.append(record_dict)
            except:
                print('Can\'t fetch article: {:s}'.format(temp_df['link'][ind]))
        self.news_df = pd.DataFrame(content_list)
        self.news_df['Date'] = pd.to_datetime(self.news_df.Date).dt.date
        self.news_df = self.news_df.sort_values(by='Date', ignore_index=True)
        self.news_df.reset_index()
    
    def search_stock_price(self):
        self.price_df = yf.download(self.ticker,
                                    start=self.start_time,
                                    end=self.end_time,
                                    group_by='ticker')
