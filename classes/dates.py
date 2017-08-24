import datetime


class Date_Maker():

    def __init__(self):
        self.dates = {'date': '',
                      'time': '',
                      4: {  # Dates for booking 4 weeks in advance
                                     'depart': '',
                                     'intl_return': '',
                                     'dom_return': '',
                                    },
                      8: {  # Dates for booking 8 weeks in advance
                                     'depart': '',
                                     'intl_return': '',
                                     'dom_return': '',
                                     },
                      }
        self.today = datetime.datetime.today()

    def get_dates(self):
        self.fill_dates()
        return self.dates

    def fill_dates(self):
        date = self.today.strftime('%Y-%m-%d')
        time = self.today.strftime('%H:%M:%S')

        four_weeks = datetime.timedelta(days=28)
        eight_weeks = datetime.timedelta(days=56)
        intl_return = datetime.timedelta(days=14)
        dom_return = datetime.timedelta(days=7)

        self.dates['date'] = date
        self.dates['time'] = time
        self.dates[4]['depart'] = (four_weeks +
                                   self.today).strftime('%Y-%m-%d')
        self.dates[4]['intl_return'] = (four_weeks + intl_return +
                                        self.today).strftime('%Y-%m-%d')
        self.dates[4]['dom_return'] = (four_weeks + dom_return +
                                       self.today).strftime('%Y-%m-%d')
        self.dates[8]['depart'] = (eight_weeks +
                                   self.today).strftime('%Y-%m-%d')
        self.dates[8]['intl_return'] = (eight_weeks + intl_return +
                                        self.today).strftime('%Y-%m-%d')
        self.dates[8]['dom_return'] = (eight_weeks + dom_return +
                                       self.today).strftime('%Y-%m-%d')
