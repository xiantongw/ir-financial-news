from DataCollector import *

if __name__ == '__main__':
    data_collector = DataCollector(ticker = 'JPM',
                                   keywords_list =['JPM'],
                                   start_time='2012-05-01',
                                   end_time='2012-05-02')
    data_collector.search_news()
    data_collector.news_df.to_csv('test.csv', index=False)