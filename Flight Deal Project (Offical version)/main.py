# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import re
from pprint import pprint
from flight_search import FlightSearch
from data_manager import DataManager
from notification_manager import NotificationManager
from datetime import datetime, timedelta

# Departure city and period of time
SUBJECT = 'There is the good deal for new flight'
MY_LOCATION = 'SGN'
MY_LOCATION_NAME = 'Ho Chi Minh'
min_date = (datetime.now() + timedelta(days=2)).strftime('%d/%m/%Y')
max_date = (datetime.now() + timedelta(weeks=24)).strftime('%d/%m/%Y')

# Create Instance
data_manager = DataManager()
flight_search = FlightSearch()
noti_manager = NotificationManager()

# Get sheet data
sheet_data = data_manager.get_sheet_data()
list_iatacode_sheet = [city['iataCode'] for city in sheet_data if 'iataCode' in city.keys()]

try:
    ask = input('Do you would like to add city (Y/Yes or N/No) ').upper()
    # use regex to valid the question
    pa = r'[Y|N|(YES)|(NO)]'
    if not re.search(pattern=pa, string=ask):
        raise TypeError
except TypeError as e:
    pprint(e)
else:

    if ask == 'Y' or ask == 'YES':
        # search city and iatia code
        city = input('Which city do you would like to travel? ')
        search_city = flight_search.search_iatacode_city(city=city)

        # check that city whether it is into sheet, if not, add that city to that sheet.
        if len(search_city) > 0 and search_city['IATAcode'] not in list_iatacode_sheet:
            response = data_manager.add_data(city=search_city['name_city'], iatacode=search_city['IATAcode'])
            pprint(response)

            # update sheet data and list_iatacode in sheet
            sheet_data = data_manager.get_sheet_data()
            list_iatacode_sheet = [city['iataCode'] for city in sheet_data if 'iataCode' in city.keys()]

        elif len(search_city) == 0:
            print('No appropriate city when calling the API')

    # Search the cheapest price
    for arrive_iata in list_iatacode_sheet:
        cheap_route = flight_search.search_cheap_price(org='SGN',
                                                       des=arrive_iata,
                                                       from_date=min_date,
                                                       to_date=max_date,
                                                       adult_number=1,
                                                       stay_days=2)

        # Add the relevant data of the flight into the sheet
        data_manager.update_flight_data(iataCode=arrive_iata,
                                        lowest_price=cheap_route.round_price,
                                        local_departure_0=cheap_route.local_departure_0,
                                        local_arrival_0=cheap_route.local_arrival_0,
                                        local_departure_1=cheap_route.local_departure_1,
                                        local_arrival_1=cheap_route.local_arrival_1,
                                        deep_link=cheap_route.deep_link,
                                        air_line_brand=cheap_route.air_line_brand)

        # Send message when detect the better deal than in the sheety
        noti_manager.create_message(price=cheap_route.round_price,
                                  de_city=cheap_route.departure_city,
                                  de_iata=cheap_route.departure_airport_code,
                                  arr_city=cheap_route.destination_city,
                                  arr_iata=cheap_route.departure_airport_code,
                                  inbound_date=cheap_route.local_departure_1.split('T')[0],
                                  outbound_date=cheap_route.local_departure_0.split('T')[0])
        noti_manager.send_message()
