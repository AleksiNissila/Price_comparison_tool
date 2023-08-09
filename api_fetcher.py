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

            name = ""
            priceCNY = 0
            i = 0
            while name != itemname:
                name = r["data"]["items"][i]["name"]
                priceCNY = r["data"]["items"][i]["sell_min_price"]
                i += 1
            i -= 1

            # Get an image for the found item
            image = self.getItemImage(r, i)

            # This could use a better way, since the image is gotten from "getPrice" atm
            return name, priceCNY, image
        except KeyError:
            print("Could not find data from Buff. (Try setting the cookies again)")
            return "noname", 0

    def getItemImage(self, r, i):
        img_url = r["data"]["items"][i]["goods_info"]["original_icon_url"]
        response = requests.get(img_url)
        print(img_url)
        image = Image.open(BytesIO(response.content))
        image.thumbnail((150, 150), Image.ANTIALIAS)
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
        priceEUR = priceEUR.replace(',', '.',).replace('-', '0',).replace(' ', '')
        print(priceEUR)
        return priceEUR