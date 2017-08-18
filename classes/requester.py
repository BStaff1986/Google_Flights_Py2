import os
import json
import requests


class JSON_Requester():
    def __init__(self, flight_details):
        # Unpack variables from flight itinerary generator
        self.orig = flight_details['Orig']
        self.dest = flight_details['Dest']
        self.today = flight_details['today']
        self.dep_date = flight_details['dep_date']
        self.ret_date = flight_details['ret_date']
        self.book = flight_details['booking']

        self.path = '.\\files\\'
        # Run functions
        payload = self.set_payload()
        url = self.get_url_with_api_key()
        self.json_ = self.send_request(url, payload)

    def set_payload(self):
        payload = {
                    "request": {
                                "passengers": {
                                                "adultCount": "1"
                                                },
                                "slice": [
                                           {  # Depart dictionary
                                            "origin": self.orig,
                                            "destination": self.dest,
                                            "date": self.dep_date,
                                            "permittedCarrier": ['AC', 'WS']
                                             },
                                           {  # Return dictionary
                                             "origin": self.dest,
                                             "destination": self.orig,
                                             "date": self.ret_date,
                                             "permittedCarrier": ['AC', 'WS']
                                             }
                                           ],
                                "solutions": "10",
                                 }
                    }
        return payload

    def get_url_with_api_key(self):
        uri = 'https://www.googleapis.com/qpxExpress/v1/trips/search'
        with open('.\\files\\requests_info\\api_key.txt') as f:
            api_key = f.read()
        return uri + '?key=' + api_key

    def check_for_json_folders(self):
        # Check and create the necessary folders
        if not os.path.isdir(self.path + '\\json\\'):
            os.mkdir(self.path + '\\json\\')
        if not os.path.isdir(self.path + '\\json\\' + self.today):
            os.mkdir(self.path + '\\json\\' + self.today)
            
    def save_json_file(self, r):
        json_data = json.loads(r.text)
        file_path = (self.path + '\\json\\' + self.today + '\\')
        file_name = (self.today + '-' + self.orig +
                     '-' + self.dest + '_' + str(self.book) + '.JSON')
        with open(file_path + file_name, 'w') as outfile:
            json.dump(json_data, outfile)
            print(file_name + ' written to hard-drive')

    def write_error_log(self, r, status_code_error=True):
        self.check_for_json_folders()
        file_path = (self.path + '\\error_logs\\')
        if not os.path.isdir(file_path):
            os.mkdir(file_path)
        
        # Status Code Error Logging
        if status_code_error:
            file_name = file_path + self.today + '_response_error_code.txt'
            with open(file_name, 'a') as f:
                f.write('\n' + str(r.status_code) + ' status code error ' +
                    'while requesting flight data for ' + self.orig + ' to ' +
                    self.dest + ' with a departure of ' + self.dep_date +
                    ' and a return of ' + self.ret_date + '\n'
                    + r.text)
            self.save_json_file(r)
            print('\tRequest Status Code: ' + str(r.status_code))
            print('\tError logged in ' + file_name)
            return None
        # Empty JSON response logging
        else:
            file_name = file_path + self.today + '_empty_JSON_returned.txt'
            with open(file_name, 'a') as f:
                f.write('\nThe flight from ' + self.orig + ' to ' + self.dest +
                        ' departing on ' + self.dep_date + ' and returning ' +
                        'on ' + self.ret_date + ' returns an empty JSON file.')
            self.save_json_file(r)
            print('\tRequest Status Code: ' + str(r.status_code))
            print('\tError logged in ' + file_name)
            return None

    def send_request(self, url, payload):
        with open('.\\files\\requests_info\\proxy_login.txt', 'r') as f:
            login =  list(iter(f))
            user = login[0].replace('\n', '')
            password = login[1].replace('\n', '')
            proxy = login[2].replace('\n', '')
        
        
        proxy_url = user +":" + password + '@' + proxy
        proxies = {
                    "https":"https://" + proxy_url,
                    "http":"http://" + proxy_url,
                    }
        
        r = requests.post(url, json=payload, proxies=proxies)
        if r.status_code == 200:
            if len(r.text) >= 300: # Less than 300 characters means error JSON
                self.check_for_json_folders()
                self.save_json_file(r)
                data = json.loads(r.text)
            else:
                data = self.write_error_log(r, status_code_error=False)
        else:
            data = self.write_error_log(r)
            
        return data

if __name__ == '__main__':
                    
    sample_dict = {'Dest': 'PEK',
                   'Orig': 'YYZ',
                   'booking': '4',
                   'dep_date': '2017-09-08',
                   'ret_date': '2017-09-22',
                   'today': '2017-08-15'}
    
    jr = JSON_Requester(sample_dict)