import requests

acceptedCurrencies = ["USD", "CNY", "EUR"]

def getConversionRate(fromRate, toRate):
    """
    Function for getting conversion rate between different currencies
    :param fromRate: Currency to be converted from
    :param toRate: Currency to be converted to
    :return: Conversion rate between fromRate and toRate
    """
    # Return None if input currencies are wrong / not found in the list
    if not (fromRate in acceptedCurrencies and toRate in acceptedCurrencies):
        return None
    else:
        if (fromRate == "CNY" and toRate == "USD"):
            r = getRate("CNY", "USD")
            rate = float(1 / r["rates"]["USDCNY"]["rate"])

        if (fromRate == "CNY" and toRate == "EUR"):
            r = getRate("CNY", "USD")
            rate1 = float(1 / r["rates"]["USDCNY"]["rate"])
            r = getRate("USD", "EUR")
            rate2 = float(1 / r["rates"]["EURUSD"]["rate"])
            rate = rate1 * rate2

        if (fromRate == "USD" and toRate == "CNY"):
            r = getRate("CNY", "USD")
            rate = float(r["rates"]["USDCNY"]["rate"])

        if (fromRate == "USD" and toRate == "EUR"):
            r = getRate("USD", "EUR")
            rate = float(1 / r["rates"]["EURUSD"]["rate"])

        if (fromRate == "EUR" and toRate == "USD"):
            r = getRate("USD", "EUR")
            rate = float(r["rates"]["EURUSD"]["rate"])

        if (fromRate == "EUR" and toRate == "CNY"):
            r = getRate("USD", "EUR")
            rate1 = float(r["rates"]["EURUSD"]["rate"])
            r = getRate("CNY", "USD")
            rate2 = float(r["rates"]["USDCNY"]["rate"])
            rate = rate1 * rate2

        return rate

def getRate(fromRate, toRate):
    """
    Function for getting a json for conversion rate between 2 currencies
    :param fromRate: Currency to be converted from
    :param toRate: Currency to be converted to
    :return: json containing the requested conversion rate
    """
    URL = "https://www.freeforexapi.com/api/live?pairs=" + toRate + fromRate
    r = requests.get(URL).json()
    return r

def convert_value(value, fromRate, toRate):
    """
    Function for fetching conversion rate and calculating the value conversion
    :param value: Value which will be converted from currency to another
    :param fromRate: Currency to be converted from
    :param toRate: Currency to be converted to
    :return: Value after conversion to another currency
    """
    conversion_rate = getConversionRate(fromRate, toRate)
    if conversion_rate != None:
        converted_value = round(float(value) * float(conversion_rate), 2)
    else:
        return None
    return converted_value

def calculate_difference(steam_val, buff_val):
    """
    Function for calculating difference in price between 2 prices
    :param steam_val: First price
    :param buff_val: Second price
    :return: Flat difference, and difference as a percentage
    """
    steam_val, buff_val = float(steam_val), float(buff_val)
    eur_diff = steam_val - buff_val
    percentage_diff = (eur_diff / steam_val) * 100
    percentage_diff = -percentage_diff
    eur_diff = round(eur_diff, 1)
    percentage_diff = round(percentage_diff, 1)

    return str(eur_diff), str(percentage_diff)