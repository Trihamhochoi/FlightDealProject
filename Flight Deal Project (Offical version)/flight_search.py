import requests
from flight_data import FlightData

KIWI_KEY = 'Ad1teJNLswiz5aYSe2-3R6eypP0IV2hp'

HEADER = {
    'apikey': KIWI_KEY,
    'Content-Type': 'application/json'
}
SEARCH_LOCATION_API = 'https://tequila-api.kiwi.com/locations/query'
SEARCH_FLIGHT_API = 'https://tequila-api.kiwi.com/v2/search'


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.header = HEADER
        self.location_api = SEARCH_LOCATION_API
        self.flight_api = SEARCH_FLIGHT_API

    # Search city to get iata code
    def search_iatacode_city(self, city):
        parameter = {
            'term': city,
            'locale': 'en-US',
            'location_types': 'city',
            'limit': 5,
            'sort': 'name'}
        try:
            con = requests.request(method='GET',
                                   url=self.location_api,
                                   headers=HEADER,
                                   params=parameter)
            con.raise_for_status()
        except Exception as e:
            return e
        else:
            data = con.json()['locations']
            list_other_city = []
            for re in data:
                if re['country']['code'] == 'VN':
                    return dict(IATAcode=re['code'],
                                name_city=re['name'],
                                country=re['country'],
                                type=re['type'])
                else:
                    other_city = dict(IATAcode=re['code'],
                                      name_city=re['name'],
                                      country=re['country'],
                                      type=re['type'])
                    list_other_city.append(other_city)
            return list_other_city

    # Search the cheapest price
    def search_cheap_price(self, org: str, des: str, from_date: str, to_date: str, stay_days: int, adult_number: int):
        parameter = {
            'fly_from': org,
            'fly_to': des,
            'date_from': from_date,  # min date of departure date format:dd/mm/YYYY
            'date_to': to_date,  # max date of departure date
            'return_from': from_date,  # min date of return date
            'return_to': to_date,  # max date of return date
            'night_in_dst_from': stay_days,  # min days stay
            'night_in_dst_to': stay_days,  # max days stay
            'flight_type': 'round',  # two values: round and oneway
            'adults': adult_number,
            'selected_cabins': 'M',  # class of cabin: M economy, W economy premium, C business, F first class
            'adult_hand_bag': '1',
            'curr': 'USD',
            'locale': 'en',
            'sort': 'price',
            'limit': 1
        }
        try:
            con = requests.request(method='GET',
                                   url=self.flight_api,
                                   headers=self.header,
                                   params=parameter)
            con.raise_for_status()
            route_data = con.json()['data'][0]
        except IndexError as e:
            return e
        else:
            flight_data = FlightData(
                round_price=route_data["price"],
                departure_city=route_data["route"][0]["cityFrom"],
                departure_airport=route_data["route"][0]["flyFrom"],
                destination_city=route_data["route"][0]["cityTo"],
                destination_airport=route_data["route"][0]["flyTo"],
                local_departure_0=route_data["route"][0]["local_departure"],
                local_arrival_0=route_data["route"][0]["local_arrival"],
                local_departure_1=route_data["route"][1]["local_departure"],
                local_arrival_1=route_data["route"][1]["local_arrival"],
                deep_link=route_data['deep_link'],
                air_line_brand=route_data['airlines'][0]
            )
            print(f'{flight_data.destination_city}:${flight_data.round_price}')
            return flight_data
