class FlightData:
    # This class is responsible for structuring the flight data.
    round_price: int
    departure_airport: str
    departure_city: str
    destination_airport: str
    destination_city: str
    local_departure_0: str
    local_arrival_0: str
    local_departure_1: str
    local_arrival_1: str
    deep_link: str
    air_line_brand: str

    def __init__(self, round_price, departure_airport, departure_city, destination_airport, destination_city, deep_link,
                 local_departure_0, local_arrival_0,local_departure_1, local_arrival_1, air_line_brand):
        self.air_line_brand = air_line_brand
        self.round_price = round_price
        self.departure_airport_code = departure_airport
        self.departure_city = departure_city
        self.destination_airport = destination_airport
        self.destination_city = destination_city
        self.deep_link = deep_link
        self.local_departure_0 = local_departure_0
        self.local_arrival_0 = local_arrival_0
        self.local_departure_1 = local_departure_1
        self.local_arrival_1 = local_arrival_1

