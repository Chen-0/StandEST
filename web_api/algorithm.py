#!/usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import pymongo
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import random


client = MongoClient('localhost', 27017)
db = client.sync
zzOrders = db["zz_orders"]
zzProducts = db["zz_products"]
zzUser = db["zz_user"]


# 相似度计算
def cos_sim(inA, inB):
    num = float(inA.T*inB)
    denom = np.linalg.norm(inA) * np.linalg.norm(inB)
    return 0.5 + 0.5 * (num / denom)


# 基于相似度的推荐算法
def standEst(dataMat, user, simMeas, item):
    n = np.shape(dataMat)[1]

    simTotal = 0.0
    ratSimTotal = 0.0
    for j in range(n):
        userRating = dataMat[user, j]
        if userRating == 0:
            continue

        overLap = np.nonzero(np.logical_and(
            dataMat[:, item] > 0, dataMat[:, j] > 0))[0]

        if len(overLap) == 0:
            similarity = 0
        else:
            similarity = simMeas(dataMat[overLap, item], dataMat[overLap, j])
        simTotal += similarity
        ratSimTotal += similarity * userRating

    if simTotal == 0:
        return 0
    else:
        return ratSimTotal / simTotal


def svdEst(dataMat, user, simMeas, item):
    n = np.shape(dataMat)[1]
    simTotal = 0.0
    ratSimTotal = 0.0
    U, Sigma, VT = np.linalg.svd(dataMat)

    svdSize = 4
    Sig4 = np.mat(np.eye(svdSize) * Sigma[:svdSize])
    xformedItems = dataMat.T * U[:, :svdSize] * Sig4.I

    for j in range(n):
        userRating = dataMat[user, j]
        if userRating == 0 or j == item:
            continue
        similarity = simMeas(xformedItems[item, :].T, xformedItems[j, :].T)
        simTotal += similarity
        ratSimTotal += similarity * userRating

    if simTotal == 0:
        return 0
    else:
        return ratSimTotal / simTotal

# 创建矩阵
def createMat(itemNoList, s, e):
    userList = zzUser.find().sort("consume_total", pymongo.DESCENDING).limit(20)

    matArray = []

    a = []
    for i in range(150):
        a.append(0)
    
    w = 1
    for item_no in itemNoList:
        p = zzProducts.find_one({"item_no": item_no})
        a[p["com_no"]] = w
        w += 1
    matArray.append(a)

    for user in userList:
        matArray.append(user["dd"])

    data = np.mat(matArray)
    return data

# 更新用户画像
def updateUserDashboard():
    items = zzUser.find()

    piLen = zzProducts.find().count()

    for xt in items:
        card_id = xt['card_id']

        saleflowList = zzOrders.find({"card_id": card_id})

        dd = []
        for k in range(piLen):
            dd.append(0)

        consume_total = 0
        for saleflow in saleflowList:
            pi = zzProducts.find_one({"item_no": saleflow["item_no"]})
            dd[pi["com_no"]] += saleflow["sale_qnty"]
            consume_total += saleflow["sale_money"]
            zzUser.update_one({
                "card_id": card_id
            }, {
                "$set": {
                    "dd": dd,
                    "consume_total": consume_total
                }
            })
        # break


def recommend(dataMat, user, N=3, simMeas=cos_sim, estMethod=standEst):
    unratedItems = np.nonzero(dataMat[user, :].A == 0)[1]
    if len(unratedItems) == 0:
        return '推荐失败'

    print("unratedItems length", len(unratedItems))

    itemScores = []

    for item in unratedItems:
        estimatedScore = estMethod(dataMat, user, simMeas, item)
        itemScores.append({
            "item": int(item),
            "score": float(estimatedScore)
        })
    items = sorted(itemScores, key=lambda x: x.__getitem__(
        'score'), reverse=True)[:N]
    return items
