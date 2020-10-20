from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
import pandas as pd
import nltk

class DataCollector:

    def __init__(self, keywords_list, start_time, end_time):
        # configure for news downloading agent
        nltk.download('punkt')
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        self.config = Config()
        self.config.browser_user_agent = user_agent

        self.keywords_list = keywords_list
        self.start_time = start_time
        self.end_time = end_time
        self.googlenews_client = GoogleNews(start=self.start_time,
                                            end=self.end_time)
        self.news_df = None

    def search_news(self, max_page=10):
        news_list = list()
        # iterate for keywords
        for keyword in self.keywords_list:
            googlenews_client = GoogleNews(start=self.start_time,
                                           end=self.end_time)
            googlenews_client.search(keyword)
            for i in range(1, max_page):
                googlenews_client.getpage(i)
            news_list = news_list + googlenews_client.result()
        # convert to pandas dataframe and remove duplicates
        temp_df = pd.DataFrame(news_list)
        temp_df.drop(['img'], inplace=True, axis=1)
        temp_df.drop(['desc'], inplace=True, axis=1)
        temp_df.drop_duplicates(subset='link', inplace=True, keep='first')
        # get text from links
        content_list = list()
        for ind in temp_df.index:
            try:
                record_dict = dict()
                article = Article(temp_df['link'][ind], config=self.config)
                article.download()
                article.parse()
                article.nlp()
                record_dict['Date']=temp_df['date'][ind]
                record_dict['Media']=temp_df['media'][ind]
                record_dict['Title']=article.title
                record_dict['Article']=article.text
                record_dict['Summary']=article.summary
                content_list.append(record_dict)
            except:
                print('Can\'t fetch article: {:s}'.format(temp_df['link'][ind]))
        self.news_df = pd.DataFrame(content_list)

