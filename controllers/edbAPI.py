#!-*- coding:utf-8 -*-
#新接口定义：
#    1、定义一个用EdbAPI装饰的方法，该方法根据需要对传入的参数进行一些必要的处理，并返回一个字典对象
#    2、定义请求结果处理函数，并加入到HandleResult总控方法中
#
#具体接口说明：
#    1、AddTrade:
#        功能:导入订单到e店宝
#        传入参数:必须是以对应的xml标签做key值的字典参数
#    2、GetBarCode:
#        功能：获取产品对应的条形码
#        传入参数:产品名称 或 {"productName":"产品名称"}
#        特殊说明:如果有多条返回值，取第一条返回值中的条形码

import os
#import sys
import time
import hashlib
#import chardet
import requests
import json
from datetime import datetime
import xml.etree.ElementTree as XML_ET

def GetTimeStamp():
    t=time.localtime()
    lst=[]
    for i in xrange(len(t)):
        if i>=5:
            break
        v=str(t[i]).zfill(2)
        lst.append(v)
    reStr="".join(lst)
    return reStr

def MD5Sign(md5Str):
    m=hashlib.md5()
    m.update(md5Str)
    return m.hexdigest().upper()

def cmp(x,y):
    x1=x.lower()
    y1=y.lower()
    if x1>y1:
        return 1
    if x1<y1:
        return -1
    return 0

def log_file(msg):
    dir=os.getcwd()
    fileName="err.txt"
    finalPath=os.path.join(dir,fileName)
    with open(finalPath,"ab") as f:
        f.write("[%s] %s\r\n"%(GetTimeStamp(),msg))
    return finalPath

def HandleAddTradeResult(data,xmlObj):
    lst=xmlObj.findall("Rows")
    if not lst:
        return False
    lst=lst[0].findall("is_success")
    if not lst:
        return False
    if lst[0].text!="True":
        print "Trade Add Fail"
        log_file("%s %s"%("edbTradeAdd",data))
        filePath=log_file(XML_ET.tostring(xmlObj))
        print "log_file in",filePath
        return False
    return True

def HandleGetBarCode(data,xmlObj):
    lst=xmlObj.findall("Rows")
    if not lst:
        return False
    lst=lst[0].findall("bar_code")
    if not lst:
        return False
    return lst[0].text

def HandleResult(method,data,xmlObj):
    if method=="edbTradeAdd":
        return HandleAddTradeResult(data,xmlObj)
    elif method=="edbProductBaseInfoGet":
        return HandleGetBarCode(data,xmlObj)
    return None

def EdbAPI(**arg):
    def _EdbAPI(func):
        def __EdbAPI(data):
            #url="http://vip79.edb04.net/edb2/rest/openapi/index.aspx"
            url="http://vip79.edb04.net/rest/index.aspx"
            SysData={
                "appkey":"5a7b7896",
                "dbhost":"edb_a77527",
                "format":"json",
                "v":2.0,
                "slencry":0,
                "Ip":"117.79.148.228",
                }
            ExData={
                "appscret":"1f5b75edd28d480e968feecbc38f2c73",
                "token":"7041e7424cb4410f8370f10a2d3a285a",
                }
            param=func(data)
            param.update(SysData)
            param["method"]=arg["method"]
            param["timestamp"]=GetTimeStamp()
            paraList=[]
            for k,v in param.items():
                if k=="appkey":
                    continue
                if not str(v):
                    continue
                paraList.append(k+str(v))
            for k,v in ExData.items():
                paraList.append(k+str(v))
            paraList.sort(cmp)
            md5Str="".join(paraList)
            md5Str=SysData["appkey"]+"appkey"+SysData["appkey"]+md5Str
            param["sign"]=MD5Sign(md5Str)
            req=requests.post(url,param)
            ct= req.content
            ct=ct.replace('\r','')
            ct=ct.replace('\n','')
            return json.loads(ct,strict=False)
        return __EdbAPI
    return _EdbAPI

@EdbAPI(method="edbProductBaseInfoGet")
def GetBarCode(data):
    if type(data)==dict:
        return data
    if type(data)==str:
        return {"productName":data}
    return {}

@EdbAPI(method="edbTradeGet")
def GetTrade(data):
    if type(data)==dict:
        return data
    if type(data)==str:
        return {"begin_time":data}
    return {}

@EdbAPI(method="edbProductGet")
def GetProduct(data):
    if type(data)==dict:
        return data
    if type(data)==str:
        return {"productName":data}
    return {}

@EdbAPI(method="edbProductBaseInfoGet")
def Getbaseinfo(data):
    if type(data)==dict:
        return data
    if type(data)==str:
        return {"productName":data}
    return {}

@EdbAPI(method="edbTradeAdd")
def AddTrade(data):
    orderTag=('out_tid','shop_id','storage_id','buyer_id','buyer_msg','buyer_email','buyer_alipay','seller_remark','consignee','address','postcode','telephone','mobilPhone','privince','city','area','actual_freight_get','actual_RP','ship_method','express','is_invoiceOpened','invoice_type','invoice_money','invoice_title','invoice_msg','order_type','process_status','pay_status','deliver_status','is_COD','serverCost_COD','order_totalMoney','product_totalMoney','pay_method','pay_commission','pay_score','return_score','favorable_money','alipay_transaction_no','out_payNo','out_express_method','out_order_status','order_date','pay_date','finish_date','plat_type','distributor_no','WuLiu','WuLiu_no','in_memo','other_remark','actual_freight_pay','ship_date_plan','deliver_date_plan','is_scorePay','is_needInvoice')
    productTag=('barCode','product_title','standard','out_price','favorite_money','orderGoods_Num','gift_Num','cost_Price','tid','product_stockout','is_Book','is_presell','is_Gift','avg_price','product_freight','shop_id','out__tid','out_productId','out_barCode','product_intro')
    orderXml=XML_ET.fromstring('<info><orderInfo></orderInfo></info>')
    productXml=XML_ET.fromstring('<product_info><product_item></product_item></product_info>')
    orderInfo=orderXml.find("orderInfo")
    itemInfo=productXml.find("product_item")

    #if not "barCode" in data:
        #d={"productName":data["product_title"],}
        #data["barCode"]=GetBarCode(d)

    for k,v in data.items():
        if k in orderTag:
            tmp=XML_ET.SubElement(orderInfo,k)
            tmp.text=v#.decode('utf8')
        if k in productTag:
            tmp=XML_ET.SubElement(itemInfo,k)
            tmp.text=v#.decode('utf8')
    orderInfo.append(productXml)
    finalStr=XML_ET.tostring(orderXml,"utf8")
    result={}
    enstr=finalStr[37:]
    enstr=enstr.replace('\n','')
    #enstr=enstr.replace('\r','')
    result["xmlValues"]=enstr
    return result

@EdbAPI(method="edbTradeAdd")
def AddBsgTrade(data):
    infos=data['product_info']
    data.pop('product_info')
    orderXml=XML_ET.fromstring('<info><orderInfo></orderInfo></info>')
    orderInfo=orderXml.find("orderInfo")

    for k,v in data.items():
        tmp=XML_ET.SubElement(orderInfo,k)
        tmp.text=v#.decode('utf8')

    product_info=XML_ET.Element('product_info')
    for info in infos:
        c=XML_ET.SubElement(product_info,'product_item')
        for i,j in info.items():
            d=XML_ET.SubElement(c,i)
            d.text=j

    orderInfo.append(product_info)
    endStr=XML_ET.tostring(orderXml,"utf8")
    finalStr=endStr[37:]
    finalStr=finalStr.replace('\n','')
    result={}
    result["xmlValues"]=finalStr
    return result


#测试用，可删除
def test_main():
    data={
    "out_tid":"33",
    "shop_id":"127",
    "mobilPhone":"18565374663",
    #"storage_id":"38",
    "buyer_msg":u"以前为左奇多圈而买包野食",
    #"postcode":"000000",
    "consignee":u"冼俊华",
    "privince":u"广东省",
    "city":u"广州市",
    "area":u"南沙区",
    "address":u"广东省广州市南沙区东涌镇太",
    #"express":"EMS",
    #"invoice_msg":"121212",
    "order_date":"2016-08-18 11:47:33",
    "barCode":"BS6924743911659",
    "product_title":u"奇多",
    #"standard":"统一规格",
    #"orderGoods_Num":"1",
    }
    data1={}
    for k,v in data.items():
        if isinstance(v,str):
            data1[k]=v.decode('utf8')
        if isinstance(v, datetime):
            data1[k] = v.isoformat()
    edb_rt=AddTrade(data1)
    print edb_rt


    """data={
    "begin_time":"2016/08/01 00:00:00",
    "end_time":"2016/08/03 00:00:00"
    }
    t=GetTrade(data)
    data={
    }
    t=GetProduct(data)

    data={}
    t=Getbaseinfo(data)"""
if __name__=="__main__":
    test_main()
    """infos=[{"avg_price": "1",
            "barCode": "33320154100037",
            "cost_Price": "2.00",
            "favorite_money": "2.00",
            "gift_Num": "0",
            "is_Book": "0",
            "is_Gift": "0",
            "is_presell": "0",
            "orderGoods_Num": "1",
            "out_tid": "bsg32",
            "out_barCode": "1",
            "out_price": "2.00",
            "out_productId": "1",
            "product_freight": "0.00",
            "product_intro": "testproductintro",
            "product_stockout": "0",
            "product_title": u"S码8片装",
            "shop__id": "125",
            "standard": "S8",
            "t_id": "B16072110573189"
        }, {
            "avg_price": "",
            "barCode": "33320154100037",
            "cost_Price": "2.00",
            "favorite_money": "2.00",
            "gift_Num": "0",
            "is_Book": "0",
            "is_Gift": "0",
            "is_presell": "0",
            "orderGoods_Num": "1",
            "out_tid": "bsg32",
            "out_barCode": "5",
            "out_price": "2.00",
            "out_productId": "5",
            "product_freight": "0.00",
            "product_intro": "testproductintro",
            "product_stockout": "0",
            "product_title": u"S码12片装",
            "shop_id": "125",
            "standard": "S12",
            "t_id": "B16072110573189"
        }]
    data0={
    "actual_freight_get": "1",
    "actual_freight_pay": "1",
    "actual_RP": "1",
    "address": u"广东广州天河天寿",
    "alipay_transaction_no": "1",
    "area": u"天河",
    "buyer_alipay": "1",
    "buyer_email": "398282040@qq.com",
    "buyer_id": "1",
    "buyer_msg": "",
    "city": u"广州",
    "consignee": u"王",
    #"deliver_date_plan": "1",
    "deliver_status": "1",
    "distributor_no": "1",
    "express": u"中通上海",
    "favorable_money": "1",
    "finish_date": "2016-07-21 10:57:31",
    "in_memo": "1",
    "invoice_money": "1",
    "invoice_msg": "1",
    "invoice_title": "1",
    "invoice_type": "1",
    "is_COD": "1",
    "is_invoiceOpened": "1",
    "is_needInvoice": "1",
    "is_scorePay": "1",
    "mobilPhone": "13524291340",
    "order_date": "2016-07-21 10:57:31",
    "order_totalMoney": "1",
    #"order_type": "1",
    "other_remark": "1111111",
    "out_express_method": "1",
    "out_order_status": "1",
    "out_payNo": "1",
    "out_tid": "bsg32",
    "pay_commission": "1",
    "pay_date": "2016-07-21 10:57:31",
    "pay_method": "1",
    "pay_score": "1",
    "pay_status": "1",
    "plat_type": "TrialCenter",
    "postcode": "201203",
    "process_status": "1",
    "product_totalMoney": "1",
    "province": u"广东",
    "return_score": "1",
    "seller_remark": "11111",
    "serverCost_COD": "1",
    #"ship_date_plan": "1",
    #"ship_method": "1",
    "shop_id": "125",
    "storage_id": "24",
    "telephone": "1",
    "tid": "1",
    #"WuLiu": "1",
    #"WuLiu_no": "1",
    "product_info":infos
    }
    unneed_field=['status','tc_return','edb_return','oti_return','wrong_reason','simid','city_class','addrbkp']
    data0={}
    buf0=db(db.bsg_trade.out_tid=='bsg29').select().as_list()
    buf1=db(db.product_info.out__tid=='bsg29').select().as_list()
    for i,j in buf0[0].items():
        if i in unneed_field:
            continue
        if j:
            if isinstance(j,str):
                data0[i]=j.decode('utf8')
            if isinstance(j, datetime):
                data0[i] = unicode(j)#.isoformat()
            if isinstance(j, long):
                data0[i] = unicode(j)
                #data0[i]=j.decode('utf8')
    info1=[]
    for it in buf1:
        data1={}
        for i,j in it.items():
            if j:
                if isinstance(j,str):
                    data1[i]=j.decode('utf8')
                if isinstance(j, datetime):
                    data1[i] = unicode(j)#.isoformat()
                if isinstance(j, long):
                    data1[i] = unicode(j)
        info1.append(data1)
    data0.update({"product_info":info1})
    data0={'province': u'\u4e0a\u6d77', 'out_tid': u'bsg29',
           'express': u'\u7533\u901a', 'area': u'\u9759\u5b89\u533a',
           'invoice_type': u'0', 'mobilPhone': u'13901614883',
           'finish_date':u'2016-07-14 06:32:05', 'consignee': u'shoyn',
           'invoice_money': u'0.00', 'shop_id': u'125',
           'city': u'\u4e0a\u6d77\u5e02', 'pay_date': u'2016-07-14 06:32:05',
           'storage_id': u'24', 'product_info': [{'t_id': u'B16071418320508',
        'is_Gift': u'0', 'gift_Num': u'0', 'out_tid': u'bsg29',
        'favorite_money': u'49.90', 'out_barCode': u'6924743918269',
        'product_intro': u'\u6842\u683c\u73cd\u81b3\u78e8\u574a\u699b\u679c\u6838\u6843\u7c89340g+\u9ed1\u829d\u9ebb\u7c89',
        'barCode': u'6924743918269', 'product_freight': u'10.00', 'standard': u'\u6842\u683c\u73cd\u81b3\u78e8\u574a\u699b\u679c\u6838\u6843\u7c89340g+\u9ed1\u829d\u9ebb\u7c89',
        'is_presell': u'0', 'orderGoods_Num': u'1', 'out_productId': u'7', 'out_price': u'49.90', 'product_stockout': u'0',
        'avg_price': u'0', 'is_Book': u'0', 'shop_id': u'125',
        'product_title': u'\u6842\u683c\u73cd\u81b3\u78e8\u574a\u699b\u679c\u6838\u6843\u7c89340g+\u9ed1\u829d\u9ebb\u7c89',
        'cost_Price': u'59.90'}], 'buyer_id': u'24', 'postcode': u'201203',
        'pay_status': u'\u5df2\u4ed8\u6b3e', 'address': u'\u4e0a\u6d77\u5e02\u9759\u5b89\u533a\u94dc\u4ec1\u8def258\u53f7\u4e5d\u5b89\u5e7f\u573a\u91d1\u5ea78C',
        'plat_type': u'TrialCenter'}
    edb_return=AddBsgTrade(data0)
    print edb_return"""




