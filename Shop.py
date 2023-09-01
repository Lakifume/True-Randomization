from System import *
import Manager
import Item
import Library
import Shard
import Equipment
import Enemy
import Room
import Graphic
import Sound
import Bloodless
import Utility

def init():
    global price_skip_list
    price_skip_list = [
        "Potion",
        "Ether",
        "Waystone"
    ]

def set_shop_price_wheight(wheight):
    global shop_price_wheight
    shop_price_wheight = Utility.wheight_exponents[wheight - 1]

def randomize_shop_prices(scale):
    for entry in datatable["PB_DT_ItemMaster"]:
        if datatable["PB_DT_ItemMaster"][entry]["buyPrice"] == 0 or entry in price_skip_list:
            continue
        #Buy
        buy_price = datatable["PB_DT_ItemMaster"][entry]["buyPrice"]
        sell_ratio = datatable["PB_DT_ItemMaster"][entry]["sellPrice"]/buy_price
        multiplier = Utility.random_weighted(1.0, 0.01, 100.0, 0.01, shop_price_wheight, False)
        datatable["PB_DT_ItemMaster"][entry]["buyPrice"] = int(buy_price*multiplier)
        datatable["PB_DT_ItemMaster"][entry]["buyPrice"] = max(datatable["PB_DT_ItemMaster"][entry]["buyPrice"], 1)
        if datatable["PB_DT_ItemMaster"][entry]["buyPrice"] > 10:
            datatable["PB_DT_ItemMaster"][entry]["buyPrice"] = round(datatable["PB_DT_ItemMaster"][entry]["buyPrice"]/10)*10
        #Sell
        if not scale:
            multiplier = Utility.random_weighted(1.0, 0.01, 100.0, 0.01, shop_price_wheight, False)
        datatable["PB_DT_ItemMaster"][entry]["sellPrice"] = int(buy_price*multiplier*sell_ratio)
        datatable["PB_DT_ItemMaster"][entry]["sellPrice"] = max(datatable["PB_DT_ItemMaster"][entry]["sellPrice"], 1)