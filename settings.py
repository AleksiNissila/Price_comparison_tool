import json
import api_fetcher
import gui


with open("config.json", "r") as f:
    config = json.load(f)

def get_currency():
    return config["Currency"]

def get_currency_list():
    currency_list = ('EUR', 'USD')
    return currency_list

def set_currency(sel):

    config["Currency"][0] = sel

    if sel == "USD":
        currency = [sel, 1]
        gui.price_fetcher.i, gui.currency = 1, "USD"
    elif sel == "GPB":
        currency = [sel, 2]
        gui.price_fetcher.i, gui.currency = 2, "GPB"
    elif sel == "EUR":
        currency = [sel, 3]
        gui.price_fetcher.i, gui.currency = 3, "EUR"

    with open("config.json", "w") as f:
        json.dump(config, f)




#TODO apply nappi että ei tarvi joka kerta katsoa mikä currency
#TODO set cookies-nappi