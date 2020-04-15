from datetime import datetime, timedelta
import algorithm as xt
import json
from bson import json_util
from bson import ObjectId
from pymongo import MongoClient
import pymongo
import numpy as np
import os
import sys
from flask import Flask, request, jsonify
app = Flask(__name__)


sys.path.append(".")


# 相似度计算


client = MongoClient('localhost', 27017)
db = client.sync
saleflowCollection = db.saleflow
productItemsCollection = db.product_items
userCollection = db.user
zzOrders = db["zz_orders"]
zzProducts = db["zz_products"]
zzUser = db["zz_user"]


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/getItems')
def getItems():
    productList = list(zzProducts.find())
    return json_util.dumps(productList)


@app.route('/estGoods', methods=['POST'])
def estGoods():
    data = request.form['items']
    dataMat = xt.createMat(json.loads(data), 1, 3)
    items = xt.recommend(dataMat, 0, N=15, estMethod=xt.standEst)
    
    for item in items:
        p = zzProducts.find_one({"com_no": item["item"]})
        print(p)
        item["item_name"] = p["item_name"]
    return json.dumps(items)


if __name__ == '__main__':
    app.run()
