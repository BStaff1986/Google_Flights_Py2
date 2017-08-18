import os
import json


class Parser():

    def __init__(self, json_, flight_details):
        self.json_ = json_
        self.trips = []
        flight_details['Date'] = flight_details.pop('today')
        try:
            trip_generator = (trip for trip in json_['trips']['tripOption'])    

            def merge_two_dicts(x, y):
                z = x.copy()
                z.update(y)
                return z
            
            for trip in trip_generator:
                overall_data = self.get_overall_data(trip, flight_details)
                segment_data = self.get_segment_data(trip)
                # self.trips.append({**x, **y}) is a better solution should 
                # Python 3.5+ ever become available
                self.trips.append(merge_two_dicts(overall_data, segment_data))

        except KeyError:
            pass
        except TypeError:
            pass

    def get_overall_data(self, trip, flight_details):
        # Convenience variables
        price = trip['pricing'][0]
        vc = self.validate_currency
        overall_dict = {}

        keys = ['saleTaxTotal', 'baseFareTotal', 'saleTotal',
                'saleFareTotal', 'ptc', 'refundable', 'Orig', 'Dest',
                'Date', 'booking']
        # By adding numbers, different actions can be take on each list item
        for i, key in enumerate(keys):
            overall_dict[key] = None
            try:
                if i <= 3:
                    overall_dict[key] = vc(price[key])
                elif i == 4 or i == 5:
                    overall_dict[key] = price[key]
                else:
                    overall_dict[key] = flight_details[key]
            except:
                continue

        # Adding some layers to the overall_dict for DataFrame formatting
        return {'Overall': {'Overall': overall_dict}}

    def get_segment_data(self, trip):
        seg_generator = (segment for segment in trip['slice'])

        seg_n = 0
        seg_dicts = {}
        for segment in seg_generator:
            map_ = {1: 'Depart',
                    2: 'Return'}

            leg_n = 0
            leg_dicts = {}
            leg_generator = (leg for leg in segment['segment'])

            for leg in leg_generator:
                leg_n += 1
                leg_data = self.get_leg_data(leg)
                leg_dicts['Leg ' + str(leg_n)] = leg_data

            if 'Leg 2' not in leg_dicts.keys():
                leg_dicts['Leg 2'] = self.get_blanks()

            seg_n += 1
            key = map_[seg_n]
            seg_dicts[key] = leg_dicts

        return seg_dicts

    def get_leg_data(self, leg):
        # Inner functions grab leg data depending on differing locations
        # within the JSON file
        def get_leg_data_first_level(key):
            leg_dict[key] = leg[key]

        def get_leg_data_second_level(key):
            leg_dict[key] = leg['leg'][0][key]

        def get_leg_data_depart_arrival_times(key):
            date, time = self.parse_datetime(leg['leg'][0][key])
            if key == 'departureTime':
                leg_dict['departureDate'] = date
                leg_dict['departureTime'] = time
            elif key == 'arrivalTime':
                leg_dict['arrivalDate'] = date
                leg_dict['arrivalTime'] = time

        def get_aircraft(key):
            aircrafts = self.json_['trips']['data']['aircraft']

            for aircraft in aircrafts:
                if aircraft['code'] == leg['leg'][0]['aircraft']:
                    leg_dict[key] = aircraft['name']
                    return

            leg_dict[key] = leg['leg'][0]['aircraft']
            return

        def get_flight_number(key):
            leg_dict[key] = (leg['flight']['carrier'] +
                             leg['flight']['number'])

        leg_dict = {}
        leg_keys = {
                     # First level keys
                     'connectionDuration': get_leg_data_first_level,
                     'cabin': get_leg_data_first_level,
                     'bookingCode': get_leg_data_first_level,
                     'bookingCodeCount': get_leg_data_first_level,
                     # Second level keys
                     'destinationTerminal': get_leg_data_second_level,
                     'originTerminal': get_leg_data_second_level,
                     'meal': get_leg_data_second_level,
                     'origin': get_leg_data_second_level,
                     'duration': get_leg_data_second_level,
                     'mileage': get_leg_data_second_level,
                     'destination': get_leg_data_second_level,
                     # Others
                     'departureTime': get_leg_data_depart_arrival_times,
                     'arrivalTime': get_leg_data_depart_arrival_times,
                     'aircraft': get_aircraft,
                     'flight_no': get_flight_number,
                     }

        for key in leg_keys.keys():
            try:
                leg_keys[key](key)
            except KeyError:
                leg_dict[key] = None

        return leg_dict

    def parse_datetime(self, datetime):
        timezone_dict = {
                         '+01:00': 'CET',
                         # '+01:30': '',
                         '+02:00': 'EET',
                         # '+02:30': '',
                         '+03:00': 'TRT',
                         '+03:30': 'IRST',
                         '+04:00': 'GST',
                         '+04:30': 'IRDT',
                         '+05:00': 'PKT',
                         '+05:30': 'IST',
                         '+06:00': 'KGT',
                         '+06:30': 'MMT',
                         '+07:00': 'THA',
                         # '+07:30': '',
                         '+08:00': 'CST',
                         '+08:45': 'CWST',
                         '+09:00': 'JST',
                         '+09:30': 'ACST',
                         '+10:00': 'AEST',
                         '+10:30': 'ACDT',
                         '+11:00': 'AEDT',
                         # '+11:30': '',
                         '+12:00': 'NZST',
                         '+12:45': 'CHAST',
                         '+13:00': 'NZDT',
                         '+13:45': 'CHADT',
                         '-01:00': 'EGT',
                         # '-01:30': '',
                         '-02:00': 'PMDT',
                         '-02:30': 'NDT',
                         '-03:00': 'ADT',
                         '-03:30': 'NST',
                         '-04:00': 'AST',
                         # '-04:30': '',
                         '-05:00': 'EST',
                         # '-05:30': '',
                         '-06:00': 'CST',
                         # '-06:30': '',
                         '-07:00': 'MST',
                         # '-07:30': '',
                         '-08:00': 'PST',
                         # '-08:30': '',
                         '-09:00': 'AST',
                         '-09:30': 'MIT',
                         '-10:00': 'CKT',
                         # '-10:30': '',
                         '-11:00': 'SST',
                         '-11:30': '',
                         '-12:00': 'BIT',
                         '-00:00': 'GMT',
                         '+00:00': 'GMT',
                         }

        end = datetime.find('T')
        date = datetime[:end]
        time = datetime[(end+1):-6]
        timezone = timezone_dict[datetime[-6:]]
        time = time + ' ' + timezone

        return date, time

    def get_blanks(self):
        blank_dict = {}
        keys = ['aircraft', 'arrivalDate', 'arrivalTime', 'bookingCode',
                'bookingCodeCount', 'cabin', 'connectionDuration',
                'departureDate', 'departureTime', 'destination',
                'destinationTerminal', 'duration', 'flight_no', 'meal',
                'mileage', 'origin', 'originTerminal', ]
        for key in keys:
            blank_dict[key] = None

        return blank_dict

    def validate_currency(self, price):
        if price[:3] == 'CAD':
            return float(price[3:])
        else:
            print('NON-CANADIAN FUNDS ' + price)
            return price

if __name__ == '__main__':

    file_path = ('H://Google-Flights-API//files//json//'
                 '2017-08-16//2017-08-16-YYC-LCY_4.JSON')

    with open(file_path, 'r') as f:
        json_ = json.load(f)

    flight_details = {'today': '2017-06-26',
                      'ret_date': '2017-07-10',
                      'booking': 4,
                      'Orig': 'YYZ',
                      'Dest': 'PEK',
                      'dep_date': '2017-06-27'}
    parser = Parser(json_, flight_details)
