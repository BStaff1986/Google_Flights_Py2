from basket import Basket_Proffer
from flight_gen import Flight_Generator
from dates import Date_Maker
from dataframe import DataFrame
from requester import JSON_Requester
from parse import Parser
import time


class Google_Flights():

    def __init__(self):
        begin = time.time()
        # Phase 1
        p1 = time.time()
        dates, df, flights = self.setup()
        # Phase 2
        p2 = time.time()
        df = self.process(flights, df)
        # Phase 3
        p3 = time.time()
        df.export_to_excel(dates)
        end = time.time()

        self.time_feedback(begin, p1, p2, p3, end)

    def setup(self):
        dates = Date_Maker().get_dates()
        df = DataFrame()
        Basket_Proffer(dates)
        flights = Flight_Generator(dates).generator
        return dates, df, flights

    def process(self, flights, df):
        for flight in flights:

            json_ = JSON_Requester(flight).json_
            trip_data = Parser(json_, flight).trips
            if trip_data:
                df.add_trip_to_dataframe(trip_data)

        return df

    def time_feedback(self, begin, p1, p2, p3, end):
        print('\n')
        print('Run Times').center(79, '*')
        print('Total Time:'.ljust(40, '.') + str(round((end - begin), 2)))
        print('Phase 1 Time:'.ljust(40, '.') + str(round((p2 - p1), 2)))
        print('Phase 2 Time:'.ljust(40, '.') + str(round((p3 - p2), 2)))
        print('Phase 3 Time:'.ljust(40, '.') + str(round((end - p3), 2)))
