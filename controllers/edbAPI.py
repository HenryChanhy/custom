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
import sys
import time
import hashlib
import chardet
import requests

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
            url="http://vip802.6x86.com/edb2/rest/index.aspx" 
            SysData={
                "appkey":"6f55e36b",
                "dbhost":"edb_a88888",
                "format":"XML",
                "v":2.0,
                "slencry":0,
                "Ip":"117.79.148.228",
                }
            ExData={
                "appscret":"adeaac8b252e4ed6a564cdcb1a064082",
                "token":"a266066b633c429890bf4df1690789a3",
                }
            param=func(data)
            param.update(SysData)
            param["method"]=arg["method"]
            param["timestamp"]=GetTimeStamp()
            #param["timestamp"]="201512161115"
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
            #md5Str=ToUTF8Str(md5Str)
            param["sign"]=MD5Sign(md5Str)
            req=requests.post(url,param)
            
            if not req.ok:
                print "requests FAIL"
                log_file("%s %s"%(arg,data))
                filePath=log_file(req.content)
                print "log_file in",filePath
                return
            xmlObj=XML_ET.fromstring(req.content)
            
            if xmlObj.findall("error_code"):
                print "respond error"
                log_file("%s %s"%(arg,data))
                filePath=log_file(req.content)
                print "log_file in",filePath
                return
            return HandleResult(arg["method"],data,xmlObj)
            
        return __EdbAPI
    return _EdbAPI

@EdbAPI(method="edbProductBaseInfoGet")
def GetBarCode(data):
    if type(data)==dict:
        return data
    if type(data)==str:
        return {"productName":data}
    return {}

@EdbAPI(method="edbTradeAdd")
def AddTrade(data):
    orderTag=('out_tid','shop_id','storage_id','buyer_id','buyer_msg','buyer_email','buyer_alipay','seller_remark','consignee','address','postcode','telephone','mobilPhone','privince','city','area','actual_freight_get','actual_RP','ship_method','express','is_invoiceOpened','invoice_type','invoice_money','invoice_title','invoice_msg','order_type','process_status','pay_status','deliver_status','is_COD','serverCost_COD','order_totalMoney','product_totalMoney','pay_method','pay_commission','pay_score','return_score','favorable_money','alipay_transaction_no','out_payNo','out_express_method','out_order_status','order_date','pay_date','finish_date','plat_type','distributor_no','WuLiu','WuLiu_no','in_memo','other_remark','actual_freight_pay','ship_date_plan','deliver_date_plan','is_scorePay','is_needInvoice')
    productTag=('barCode','product_title','standard','out_price','favorite_money','orderGoods_Num','gift_Num','cost_Price','tid','product_stockout','is_Book','is_presell','is_Gift','avg_price','product_freight','shop_id','out_tid','out_productId','out_barCode','product_intro')
    orderXml=XML_ET.fromstring('<info><orderInfo></orderInfo></info>')
    productXml=XML_ET.fromstring('<product_info><product_item></product_item></product_info>')
    orderInfo=orderXml.find("orderInfo")
    itemInfo=productXml.find("product_item")
    
    if not "barCode" in data:
        d={"productName":data["product_title"],}
        data["barCode"]=GetBarCode(d)

    for k,v in data.items():
        if k in orderTag:
            tmp=XML_ET.SubElement(orderInfo,k)
            tmp.text=v.decode('utf8')
        if k in productTag:
            tmp=XML_ET.SubElement(itemInfo,k)
            tmp.text=v.decode('utf8')
    orderInfo.append(productXml)
    finalStr=XML_ET.tostring(orderXml,"utf8")
    result={}
    result["xmlValues"]=finalStr
    return result


#测试用，可删除
def test_main():
    data={
    "out_tid":"CRMJ2015120728547",
    "shop_id":"15",
    "storage_id":"13",
    "buyer_id":"莫晓燕",
    "postcode":"000000",
    "privince":"河北省",
    "city":"沧州市",
    "area":"长河区",
    "express":"EMS",
    "invoice_msg":"121212",
    "order_date":"2015-12-10 13:00:00",
#    "barCode":"1",
    "product_title":"测试修改没",
    "standard":"统一规格",
    "orderGoods_Num":"1",
    }
    print AddTrade(data)
    
if __name__=="__main__":
    test_main()
    