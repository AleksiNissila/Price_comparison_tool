import json

class Inventory:
    def __init__(self):
        self.aaa = 0

    def addItem(self, id, name, amount, date, buy_price):
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

