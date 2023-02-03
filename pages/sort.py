import traceback
import logging


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
        date = flight['departure_date'].date()
        if date in flight_by_date:
            flight_by_date[flight['departure_date'].date()] += 1
        else:
            flight_by_date[flight['departure_date'].date()] = 1

    # sort dict by date
    flight_by_date = dict(sorted(flight_by_date.items(), key=lambda item: item[0]))
    return flight_by_date


def sorted_payments(payments):
    try:
        sorted_payments = []
        for pay in payments:
            refill = pay['Refill']
            agent = pay['Agent']
            user = pay['User']

            payment_dict = {
                "id": refill.id,
                "created_at": refill.created_at.strftime("%Y-%m-%d %H:%M"),
                "agent": agent.company_name,
                "user": user.username,
                "amount": refill.amount,
                "comment": refill.comment
            }
            sorted_payments.append(payment_dict)
        return sorted_payments

    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


def sorted_agents(agents):
    """ id, fullname, discount """
    try:
        sort_agents = []
        for agen in agents:
            agent = agen['Agent']
            discount = agen['Discount']
            user = agen['User']

            agent_dict = {
                "id": agent.id,
                "name": agent.company_name,
                "login": user.email,
                "discount": discount.amount,
                "discount_name": discount.name,
                "balance": agent.balance,
                "is_on_credit": agent.is_on_credit,
            }
            sort_agents.append(agent_dict)
        return sort_agents
    except Exception as e:
        print(logging.error(traceback.format_exc()))
        print(logging.error(e))


if __name__ == "__main__":
    pass
