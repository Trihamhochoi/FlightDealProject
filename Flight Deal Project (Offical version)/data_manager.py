import requests

ENDPOINT = 'https://api.sheety.co/3c4c56157ba044a2b8871cb74f6d976f/flightDealProject/flightdeals'
SHEETY_KEY = 'Basic dHJpbG5kNzA2MjpQYXNzd29yZEAxMjM='
HEADER = {
    'Authorization': SHEETY_KEY,
    'Content-Type': 'application/json'
}


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.sheet_data = None
        self.header = HEADER
        self.endpoint = ENDPOINT

    def get_sheet_data(self):
        try:
            connection = requests.request(method='GET',
                                          url=self.endpoint,
                                          headers=self.header)
            connection.raise_for_status()
            self.sheet_data = connection.json()['flightdeals']
            return self.sheet_data
        except Exception as e:
            return e

    def add_data(self, city, iatacode=None):
        try:
            json_data = {'flightdeal': {'city': city,
                                        'iataCode': iatacode,
                                        'lowestPrice': None,
                                        'dateFlight': None}}

            connection = requests.request(method='POST',
                                          url=self.endpoint,
                                          headers=self.header,
                                          json=json_data)
            connection.raise_for_status()
            response = connection.text
            return response
        except Exception as e:
            return e

    def update_iata_code(self, city_name, update_iata_code):
        update_json = {'flightdeal': {'iataCode': update_iata_code}}
        for city in self.sheet_data:
            if city['city'] == city_name:
                con = requests.request('PUT',
                                       url=f'{self.endpoint}/{city["id"]}',
                                       headers=self.header,
                                       json=update_json)
                con.raise_for_status()
                print(con.text)

    def update_flight_data(self, iataCode: str, lowest_price: int, local_departure_0: str, local_arrival_0: str,
                     local_departure_1: str, local_arrival_1: str,
                     deep_link: str, air_line_brand: str):
        update_json = {'flightdeal':{
            'lowestPrice': lowest_price,
            'departureDatetimeFlight1': local_departure_0,
            'arrivalDatetimeFlight1': local_arrival_0,
            'departureDatetimeFlight (return)': local_departure_1,
            'arrivalDatetimeFlight (return)': local_arrival_1,
            'bookingLink': deep_link,
            'airlineBrand': air_line_brand}}
        for city in self.sheet_data:
            if city['iataCode'] == iataCode:
                try:
                    con = requests.request('PUT',
                                           url=f'{self.endpoint}/{city["id"]}',
                                           headers=self.header,
                                           json=update_json)
                    con.raise_for_status()
                except Exception as e:
                    print(e)
                else:
                    print(con.text, end='\n\n')
