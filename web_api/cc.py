import numpy as np
import pymongo
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime,timedelta

import xt

client = MongoClient('localhost', 27017)
db = client.sync
saleflowCollection = db.saleflow
productItemsCollection = db.product_items
userCollection = db.user

zzOrders = db["zz_orders"]
zzProducts = db["zz_products"]
zzUser = db["zz_user"]

def resetOrder():
    items = zzProducts.find()

    index = 0;
    for item in items:
        zzProducts.update_one({"_id": ObjectId(item["_id"])},
        {
            "$set": {
                "com_no": index
            }
        }
        )
        index += 1

def copyProducts():
  sList = saleflowCollection.aggregate([
  {"$group": {
  "_id": "$item_no",
  "qty": {"$sum": "$sale_money"}
  }},

  {"$sort": {"qty": -1}},
  {"$limit": 150}
  ])

  for s in sList:
    #复制商品信息
    it = productItemsCollection.find_one({"item_no": s["_id"]})
    zzProducts.insert_one({
    "item_no": it["item_no"],
    "item_name": it["item_name"],
    })

def copyOrders():
  pList = zzProducts.find()

  for p in pList:
    sList = saleflowCollection.find({"item_no": p["item_no"]})
    for s in sList:
          zzOrders.insert_one({
      "item_no": s["item_no"],
      "sale_qnty": s["sale_qnty"],
      "sale_money": s["sale_money"],
      "card_id": s["card_id"],
      "created_at": s["created_at"],
      "com_no": s["com_no"],
    })

def copyUser():
  cList = zzOrders.aggregate([
  {"$group": {"_id": "$card_id"}}])

  for c in cList:
    zzUser.insert_one({"card_id": c["_id"]})

def main():
  xt.main()
  # copyUser()

    # resetOrder()



if __name__ == '__main__':
    main()



def str2time(oper_date):
    timestr = oper_date
    timestr = timestr.replace("T", " ")
    timestr = timestr.replace("Z", "")
    a = datetime.strptime(timestr, "%Y-%m-%d %H:%M:%S.%f")-timedelta(hours=8)
    return a