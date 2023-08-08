#import buff_api
#import steam_api
import requests
import currency_converter
import json
from PIL import Image, ImageTk
from io import BytesIO

with open("config.json", "r") as f:
    config = json.load(f)

class Price:
    def __init__(self):
        self.buff = Buff(config["Cookies"])
        self.steam = Steam()

    def fetch_price(self, itemname):
        buff_name, buff_price, image = self.buff.getBuffPrice(itemname)
        steam_price = self.steam.getSteamPrice(itemname)[:-1]
        return buff_name, buff_price, steam_price, image


class Buff:
    def __init__(self, header):
        self.header = {
            "Cookie": str(header)
        }
    def getBuffPrice(self, itemname):
        try:
            URL = "https://buff.163.com/api/market/goods?"
            params = {
                "game" : "csgo",
                "page_num" : "1",
                "search" : str(itemname)
            }
            r = requests.get(URL, params=params, headers=self.header).json()


            # Some search terms include both normal and
            # Stat-Trak version of the weapon.
            # This check makes sure that the search term and the found item match
            # (Because searching for non-stattrak weapon
            # might return the stattrak version otherwise)
            # TODO change this to a loop to find the wanted item.
            # Search terms such as "★ Ursus Knife" can cause problems because it returns
            # all ursus knife skins.
            name = r["data"]["items"][0]["name"]
            if name != itemname:
                name = r["data"]["items"][1]["name"]
                priceCNY = r["data"]["items"][1]["sell_min_price"]
            else:
                priceCNY = r["data"]["items"][0]["sell_min_price"]

            # Get an image for the found item
            image = self.getItemImage(r)

            # This could use a better way, since the image is gotten from "getPrice" atm
            return name, priceCNY, image
        except KeyError:
            print("Could not find data from Buff. (Try setting the cookies again)")
            return "noname", 0

    def getItemImage(self, r):
        img_url = r["data"]["items"][0]["goods_info"]["original_icon_url"]
        response = requests.get(img_url)
        print(img_url)
        image = Image.open(BytesIO(response.content))
        image.thumbnail((100, 100), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        return image



class Steam:
    rate = 1

    def getSteamPrice(self, itemname):
        URL = "https://steamcommunity.com/market/priceoverview/?appid=730"
        params = {
            "currency" : "3",
            "market_hash_name" : itemname
        }
        r = requests.get(URL, params=params).json()

        priceEUR = str(r["lowest_price"])
        priceEUR = priceEUR.replace(',', '.').replace('-', '0')
        print(priceEUR)
        return priceEUR