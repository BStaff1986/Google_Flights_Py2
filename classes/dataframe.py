import pickle
import pprint

import os
import pandas as pd


class DataFrame():

    def __init__(self):
        self.df = pd.DataFrame()

    def create_dataframe(self, trip):
        # This tricky nested dictionary comprehension creates a dict_key path
        # to every value in the trip data dictionary.
        # Ie. ('Depart', 'Leg_1', 'carrier')
        column_indices = {(direction, leg_number, data_point): [value]
                          for direction, all_trip_data in trip.items()
                          for leg_number, leg_dict in all_trip_data.items()
                          for data_point, value in leg_dict.items()}.keys()

        order = self.get_df_column_order(column_indices)

        cols = pd.MultiIndex.from_tuples(tuple(order))

        return pd.DataFrame(columns=cols)

    def get_df_column_order(self, col_idx):
        # These lists below contain the order of the DataFrame columns
        # To change the order of the DataFrame, change the order in the lists
        leg_order = ['flight_no', 'origin', 'destination', 'departureDate',
                     'departureTime', 'arrivalDate', 'arrivalTime', 'aircraft',
                     'cabin', 'meal', 'duration', 'mileage',
                     'connectionDuration', 'originTerminal',
                     'destinationTerminal', 'bookingCode', 'bookingCodeCount'                     
                     ]
        overall_order = ['Date', 'Orig', 'Dest', 'booking', 'saleTotal',
                         'baseFareTotal', 'saleFareTotal', 'saleTaxTotal',
                         'ptc', 'refundable']

        # Pairing dictionary values with the number of its position in
        # the list. (Ex. 'carrier' : 0 because carrier is first for each leg)
        leg_map = dict(zip(leg_order, range(len(leg_order))))
        overall_map = dict(zip(overall_order, range(len(overall_order))))

        # Assigning fixed value lists to keep the correct form for DF import
        overall = [None] * len(overall_order)
        depart_leg1 = [None] * len(leg_order)
        depart_leg2 = [None] * len(leg_order)
        return_leg1 = [None] * len(leg_order)
        return_leg2 = [None] * len(leg_order)

        # Puts each column index into its proper list in the proper order
        for column in col_idx:
            if column[0] == 'Overall':
                overall[overall_map[column[2]]] = column
            elif column[0] == 'Depart':
                if column[1] == 'Leg 1':
                    depart_leg1[leg_map[column[2]]] = column
                elif column[1] == 'Leg 2':
                    depart_leg2[leg_map[column[2]]] = column
            elif column[0] == 'Return':
                if column[1] == 'Leg 1':
                    return_leg1[leg_map[column[2]]] = column
                elif column[1] == 'Leg 2':
                    return_leg2[leg_map[column[2]]] = column

        return overall + depart_leg1 + depart_leg2 + return_leg1 + return_leg2

    def add_trip_to_dataframe(self, trips):
        if len(self.df) == 0:
            self.df = self.create_dataframe(trips[0])

        for trip in trips:
            reform = {(direction, leg_number, data_point): value
                      for direction, all_trip_data in trip.items()
                      for leg_number, leg_dict in all_trip_data.items()
                      for data_point, value in leg_dict.items()}
            self.df = self.df.append(reform, ignore_index=True)

    def export_to_excel(self, dates):
        file = self.get_file_name('xlsx', dates)
        self.df.to_excel(file)

    def export_to_csv(self, dates):
        file = self.get_file_name('csv', dates)
        self.df.to_csv(file, index=False)

    def get_file_name(self, file_type, dates):
        date = dates['date']
        n = ''
        dir_ = './files/flight_results/'
        f_type = file_type
        file = dir_ + str(date) + '_GoogleAPI{}.'.format(n) + f_type

        if os.path.isfile(file):
            n = 2
            while True:
                file = dir_ + str(date) + '_GoogleAPI ({}).'.format(n) + f_type
                if os.path.isfile(file):
                    n += 1
                else:
                    return file
        else:
            return file

if __name__ == '__main__':
    with open('trip_data.p', 'rb') as f:
        trip_data = pickle.load(f)
        
    df = DataFrame()
    df.add_trip_to_dataframe(trip_data)