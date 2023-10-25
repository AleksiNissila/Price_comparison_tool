import json

class Inventory:
    def __init__(self):
        self.aaa = 0

    def addItem(self, id, name, amount, date, buy_price):
        """
        Function for adding an item to inventory.json
        :param id: Id for the item
        :param name: Name for the item
        :param amount: Amount of the item
        :param date: Date for the item (e.g. when it was bought)
        :param buy_price: Initial price for the item
        :return: nothing
        """
        new_item = {"itemId" : id,
                    "name" : name,
                    "amount" : amount,
                    "date" : date,
                    "buy_price" : buy_price,
                    "latets_price" : 0}
        with open("inventory.json", "r+") as inv:
            invJson = json.load(inv)
            invJson.append(new_item)
            inv.seek(0)
            json.dump(invJson, inv, indent = 4)
        inv.close()

    def editItem(self, id, loc, new_val):
        pass

    def deleteItem(self, id):
        """
        Function for deleting an item from inventory.json
        :param id: Id for the item in the JSON-file
        :return: nothing
        """
        with open("inventory.json", "r+") as inv:
            inv_json = json.load(inv)

            for i in range(len(inv_json)):
                if(inv_json[i]["itemId"] == id):
                    del inv_json[i]
                    break

            #invJson = [obj for obj in invJson if obj['itemId'] != id]
            inv.seek(0)
            open("inventory.json", "w").close()
            json.dump(inv_json, inv, indent=4)
        #inv.seek(0)


    # def fetchPrice(self, name)

