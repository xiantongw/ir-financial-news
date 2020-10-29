import os
from datetime import date, datetime
import time

from tqdm import tqdm

from DataCollector import *


def to_isocal(date_str):
    return datetime.strptime(date_str,
                             '%Y-%m-%d').strftime('%G-W%V')


def days_in_isoweek(iso_week_str):
    '''
    return a list of dates in an iso calendar week
    '''
    return [datetime.strftime(
            datetime.strptime('{:s}-{:d}'.format(iso_week_str, iday),
                              '%G-W%V-%u'),
            '%Y-%m-%d') for iday in range(1, 8)]


def num_iso_week(year_str):
    return date(int(year_str), 12, 28).isocalendar()[1]


def download_news_by_week(ticker_in, iso_week_str):
    # save the file to the downloaded_news directory
    save_path = './downloaded_news/{:s}/'.format(ticker_in)
    if not os.path.isdir('downloaded_news'):
        os.mkdir('downloaded_news')
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    days_list = days_in_isoweek(iso_week_str)
    data_collector = DataCollector(ticker=ticker_in,
                                   start_time=days_list[0],
                                   end_time=days_list[-1])
    data_collector.search_news()
    data_collector.news_df.to_csv('{:s}/{:s}_{:s}.csv'
                                  .format(save_path,
                                          ticker_in,
                                          iso_week_str))


if __name__ == '__main__':
    # generate the list of years and weeks
    week_list = list()
    for year in range(2010, 2020):
        for week in range(1, num_iso_week(year) + 1):
            week_list.append('{:d}-W{:d}'.format(year, week))
    pbar = tqdm(week_list, ncols=120)
    for week_str in pbar:
        pbar.set_description(week_str)
        download_news_by_week('JPM', week_str)
        time.sleep(30)
