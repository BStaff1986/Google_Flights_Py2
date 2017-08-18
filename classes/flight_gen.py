import pandas as pd
import os


class Flight_Generator():

    def __init__(self, dates):
        self.dates = dates
        self.path = '.\\files'
        city_pairs = self.read_csv_to_iterrows()
        dict_list = self.set_dictionaries(city_pairs, dates)
        self.generator = self.get_generator(dict_list)

    def read_csv_to_iterrows(self):
        date = self.dates['date']
        try:
            df = pd.read_csv(self.path + '\\flight_basket\\basket.csv')
            return df.iterrows()
        except OSError:
            path = self.path + '\\error_logs\\'
            with open(path + date + '_missing_basket.txt', 'a') as f:
                f.write('basket.csv did not exist in the flight_basket dir \n')
            raise OSError('Basket file not found')

    def extract_dates(self, x, dates, return_days):
        '''
        Using a mapping, the proper values are extracted from the dates
        dictionary and then returned
        '''
        map_ = {
               0: 4,
               1: 8,
               7: 'dom_return',
               14: 'intl_return',
               }

        keys = ['today',
                'dep_date',
                'ret_date',
                'booking',
                ]

        values = [
                dates['date'],
                dates[map_[x]]['depart'],
                dates[map_[x]][map_[return_days]],  # Intl or Dom Return?
                map_[x]
                     ]

        date_dict = {}
        for k, v in zip(keys, values):
            date_dict[k] = v

        return date_dict

    def set_dictionaries(self, city_pairs, dates):
        dict_list = []

        for city in city_pairs:
            for x in range(2):  # 0 is 4 week booking, 1 is 8 weeks.
                dict_ = {}

                for key in ['Orig', 'Dest']:
                    dict_[key] = city[1][key]

                return_days = city[1]['Return']
                date_dict = self.extract_dates(x, dates, return_days)
                dict_.update(date_dict)
                dict_list.append(dict_)

        return dict_list

    def get_generator(self, dict_list):
        generator = (itinerary for itinerary in dict_list)
        return generator

if __name__ == '__main__':
    os.chdir('C:\\Users\\Bryan\\Anaconda3\\Python Projects\\Stats Canada'
             '\\Travel\\TDD\\Google')
    from classes.date_maker.Date_Maker import Date_Maker
    dates = Date_Maker().get_dates()
    fg = Flight_Generator(dates)
