#!-*- coding:utf-8 -*-

#新接口定义：
#    1、定义一个用TrialAPI装饰的方法，该方法根据需要对传入的参数进行一些必要的处理，并返回一个字典对象
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

def GetTimeStamp_edb():
    t=time.localtime()
    lst=[]
    for i in xrange(len(t)):
        if i>=5:
            break
        v=str(t[i]).zfill(2)
        lst.append(v)
    reStr="".join(lst)
    return reStr

def GetTimeStamp():
    return int(time.time())

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

def HandleUpdateTOS(data,xmlObj):
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

def HandleUpdateOTI(data,xmlObj):
    lst=xmlObj.findall("Rows")
    if not lst:
        return False
    lst=lst[0].findall("bar_code")
    if not lst:
        return False
    return lst[0].text

def HandleResult(method,data,xmlObj):
    if method=="updateOrderTrackingInfo":
        return HandleUpdateOTI(data,xmlObj)
    elif method=="updateTrialOrderStatus":
        return HandleUpdateTOS(data,xmlObj)
    return None

def TrialAPI(**arg):
    def _TrialAPI(func):
        def __TrialAPI(data):
            #url="http://vip802.6x86.com/edb2/rest/index.aspx"
            SysData={
                "apiKey":"A6BEA59B",
                }
            ExData={
                "apiSecret":"1F6F088755B094DDAD3C7AEFEA73A1A1",
                }
            param=func(data)
            param.update(SysData)
            param.update(data)
            #url="http://IP+PORT/TrialCenter/order/Pampers/ST/"+arg["method"]
            url="https://int.taotonggroup.com/pampers1/default/"+arg["method"]
            #param["method"]=arg["method"]
            param["timestamp"]=GetTimeStamp()
            #param["timestamp"]="201512161115"
            paraList=[]
            for k,v in param.items():
#                if k=="appkey":
#                    continue
                if isinstance(v,str):
                    paraList.append(k+"="+str(v))

#            for k,v in ExData.items():
#                paraList.append(k+"="+str(v))

            paraList.sort(cmp)
            md5Str="&".join(paraList)
            md5Str=md5Str+ExData["apiSecret"]
            #md5Str=ToUTF8Str(md5Str)
            param["sig"]=MD5Sign(md5Str)
            req=requests.post(url,param,verify=False)

            if not req.ok:
                print "requests FAIL"
                log_file("%s %s"%(arg,data))
                filePath=log_file(req.content)
                print "log_file in",filePath
                return
            xmlObj=XML_ET.fromstring(req.content)

            if xmlObj.findall("error"):
                print "respond error"
                log_file("%s %s"%(arg,data))
                filePath=log_file(req.content)
                print "log_file in",filePath
                return
            return HandleResult(arg["method"],data,xmlObj)

        return __TrialAPI
    return _TrialAPI

@TrialAPI(method="updateOrderTrackingInfo")
def updateOTI(data):

    return {}

@TrialAPI(method="updateTrialOrderStatus")
def updateTOS(data):

    return {}
@TrialAPI(method="TradeAdd")
def addTrade(data):

    return {}

#测试用，可删除
def test_main():
    data={
	"mobile": "1111111",
	"order_id": "1234",
	"status": "1"
    }
    print updateTOS(data)

    orderinfo={
	"order_id": "11212",
	"tracking_number": "121212121212121",
	"tracking_company": "ZTO"
    }
    print updateOTI(orderinfo)
def test_addTrade():
    data0={"product_totalMoney":"0","storage_id":"11",
       "deliver_status":"\u672a\u53d1\u8d27","consignee":"\u6d4b\u8bd51",
       "actual_RP":"","express":"\u4e2d\u901a\u4e0a\u6d77",
       "pay_status":"\u5df2\u4ed8\u6b3e","invoice_type":"","city":"\u65e0\u9521",
       "is_invoiceOpened":"0","timestamp":"1451903037","buyer_email":"",
       "area":"\u6ee8\u6e56\u533a","province":"\u6c5f\u82cf",
       "process_status":"\u672a\u786e\u8ba4","order_date":"yyyy-mm-dd hh24:mi:ss",
       "mobilPhone":"18651515873","order_totalMoney":"0","buyer_id":"","shop_id":"9",
       "invoice_title":"","out_tid":"1","postcode":"","buyer_alipay":"","pay_method":"",
       "actual_freight_get":"","address":"\u6c5f\u82cf \u65e0\u9521 \u6ee8\u6e56\u533a \u9526\u6eaa\u8def",
       "pay_date":"","invoice_money":"","invoice_msg":"",
       "product_info":[{"orderGoods_Num":"1","out__tid":"1","product_title":"\u6d4b\u8bd5\u5546\u54c11","standard":"1","cost_Price":"0","barCode":"12345678"}],
       "sig":"6b1e5af7b119bdeb1c7dc70512a6be8e","order_type":"\u6b63\u5e38\u8ba2\u5355",
       "finish_date":""}
    for k,v in data0.items():
        if isinstance(v,str):
            data0[k]=v.decode("unicode-escape")
    print addTrade(data0)
if __name__=="__main__":
    test_main()
