#!-*- coding:utf-8 -*-
__author__ = 'Administrator'

import json
import requests

url="http://wdapi.9mds.com/json/reply/UpdateOrderStatusReq"
data0={
    "model": {
        "id": 28,
        "express_id": 3,
        "express_no": "407921927962"
    }
}

req=requests.post(url,data0)
req.content



