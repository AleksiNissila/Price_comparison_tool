import json


with open("config.json", "r") as f:
    config = json.load(f)

def get_currency():
    return config["Currency"]

def get_currency_list():
    currency_list = ('EUR', 'USD')
    return currency_list

def set_currency(sel):
    config["Currency"] = sel
    with open("config.json", "w") as f:
        json.dump(config, f)

#TODO apply nappi että ei tarvi joka kerta katsoa mikä currency