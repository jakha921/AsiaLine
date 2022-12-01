from logics import api
from app import crud as user_crud
from crud_models import crud


def sort_currency_rate(currency_rate):
  
    dict_currency_rate = {
      "RUBUSD": currency_rate.rub_to_usd,
      "RUBEUR": currency_rate.rub_to_eur,
      "RUBUZS": currency_rate.rub_to_uzs,
      "updated_at": currency_rate.updated_at.strftime("%Y-%m-%d %H:%M:%S")
      }

    return dict_currency_rate


def sort_by_date_flights(flights):
  
    # count flights by same date
    flight_by_date = {}
    for flight in flights:
        flight.departure_date = flight.departure_date.date()
        if flight.departure_date in flight_by_date:
            flight_by_date[flight.departure_date] += 1
        else:
            flight_by_date[flight.departure_date] = 1
            
    # sort dict by date
    flight_by_date = dict(sorted(flight_by_date.items(), key=lambda item: item[0]))
    return flight_by_date


def sort_airport(db, airport_id):
  airport = crud.Airport.get_by_id(db, airport_id)
  
  airport_dict = {
    "id": airport.id,
    "airport_ru": airport.airport_ru,
    "airport_en": airport.airport_en,
    "airport_uz": airport.airport_uz,
    "city": {
      "id": airport.city_id,
      "city_ru": airport.city.city_ru,
      "country": {
        "id": airport.city.country_id,
        "country_ru": airport.city.country.country_ru,
        } 
      }
    }
  
  return airport_dict


# def sort_flights(db, flights):
  # print(flights)
  # flight = {}
  
  # for numb, _ in enumerate(flights):
  #   from_airport = sort_airport(db, flights[numb].from_airport_id)
  #   for nb, i in enumerate(from_airport):
  #     flight['id'] = i[0][nb].id
      # flight['flight_name'] = i.flight_number
      # flight['from_airport'] = sort_airport(db, i.from_airport_id)
      # flight['to_airport'] = sort_airport(db, i.to_airport_id)
      # flight['departure_date'] = i.departure_date.strftime("%Y-%m-%d %H:%M:%S")
      # flight['arrival_date'] = i.arrival_date.strftime("%Y-%m-%d %H:%M:%S")
      # flight['price'] = i.price
      # flight['currency'] = i.currency
      # flight['total_seats'] = i.total_seats
      # flight['left_seats'] = i.left_seats
      # flight['on_sale'] = i.on_sale.strftime("%Y-%m-%d %H:%M:%S")
      # flight['actor_id'] = user_crud.User.get_by_id(db, i.actor_id)
      # flight['created_at'] = i.created_at
      # flight['updated_at'] = i.updated_at
      # flight['deleted_at'] = i.deleted_at

  return 1

def group_flights(db, flights):
  group_flights = {}
  for flight in flights:
    from_airport = sort_airport(db, flight.from_airport_id)
    to_airport = sort_airport(db, flight.to_airport_id)
    key = f"{from_airport['airport_ru']} > {to_airport['airport_ru']}"
    if key in group_flights:
      group_flights[key].append(flight)
    else:
      group_flights[key] = [flight]
  
  # sort dict by key
  group_flights = dict(sorted(group_flights.items(), key=lambda item: item[0]))
  
  # sort flights by departure_date
  for key, value in group_flights.items():
    group_flights[key] = sorted(value, key=lambda x: x.departure_date)
  
  return group_flights


if __name__ == "__main__":
    pass