import json
import api_fetcher
import gui


with open("config.json", "r") as f:
    config = json.load(f)

def get_currency():
    """
    function for getting currency value from config-file
    :return: currency value from config-file
    """
    return config["Currency"]

def get_currency_list():
    """
    function for getting currency list
    :return: currency list
    """
    currency_list = ('EUR', 'USD')
    return currency_list

def set_currency(sel):
    """
    Function for setting currency into price_fetcher and GUI
    :param sel: selected currency
    :return: nothing
    """
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

