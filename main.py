from DataCollector import *

if __name__ == '__main__':
    data_collector = DataCollector(keywords_list =['JPM'],
                                   start_time='05/01/2012',
                                   end_time='05/31/2012')
    data_collector.search_news()
    data_collector.news_df.to_excel('test.xlsx')