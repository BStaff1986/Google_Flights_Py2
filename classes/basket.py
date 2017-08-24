import os
import pandas as pd


class Basket_Proffer():

    def __init__(self, dates):
        self.dates = dates
        self.path = '.\\files'
        file_path = self.path + '\\flight_basket\\basket.csv'
        if not os.path.isfile(file_path):
            self.df = self.read_in_excel()
            self.df = self.convert_to_iata_code(self.df)
            self.to_csv(self.df)

    def read_in_excel(self):
        file_path = self.path + '\\flight_basket\\flight_basket.xlsx'
        print(os.listdir(file_path))
        if os.path.isfile(file_path):
            df = pd.read_excel(file_path)
            df.drop('Area', axis=1, inplace=True)
            return df
        else:
            raise OSError('The file flight_basket.xlsx is missing '
                          'from the flight_basket directory. Please '
                          'replace it and try again!')

    def convert_to_iata_code(self, df):
        airport_codes = {
                    'Amsterdam': 'AMS',
                    'Athens': 'ATH',
                    'Barcelona': 'BCN',
                    'Beijing': 'PEK',
                    'Calgary': 'YYC',
                    'Cancun': 'CUN',
                    'Dublin': 'DUB',
                    'Charlottetown': 'YYG',
                    'Edmonton': 'YEG',
                    'Frankfurt': 'FRA',
                    'Fredricton': 'YFC',
                    'Fort Lauderdale': 'FLL',
                    'Halifax': 'YHZ',
                    'Hong Kong': 'HKG',
                    'Honolulu': 'HNL',
                    'Kahului': 'OGG',
                    'Las Vegas': 'LAS',
                    'Lisbon': 'LIS',
                    'London': 'LCY',
                    'Los Angeles': 'LAX',
                    'Miami': 'MIA',
                    'Moncton': 'YQM',
                    'Montreal': 'YUL',
                    'Orlando': 'MCO',
                    'Ottawa': 'YOW',
                    'Palm Springs': 'PSP',
                    'Paris': 'CDG',
                    'Puerto Vallarta': 'PVR',
                    'Punta Cana': 'PUJ',
                    'Regina': 'YQR',
                    'Rome': 'CIA',
                    'Saskatoon': 'YXE',
                    'Shanghai': 'PVG',
                    "St. John's": 'YYT',
                    'Sydney': 'SYD',
                    'Thunder Bay': 'YQT',
                    'Toronto': 'YYZ',
                    'Vancouver': 'YVR',
                    'Varadero': 'VRA',
                    'Winnipeg': 'YWG',
                    }

        df_len = len(df)
        segments = ['Orig', 'Dest']
        for segment in segments:
            df[segment] = df[segment].map(airport_codes)
        df.dropna(inplace=True)

        count = df_len - len(df)
        if count > 0:
            self._write_to_error_log(count)

        return df

    def _write_to_error_log(self, count):
            date = self.dates['date']
            path = self.path + '\\error_logs\\'
            with open(path + date + '_dropped_flights.txt', 'a') as f:
                f.write(str(count) + ' unrecognized city(or cities) in '
                        'the flight_basket.xlsx file. \n')

    def to_csv(self, df):
        df.to_csv(self.path + '\\flight_basket\\basket.csv', index=False)
