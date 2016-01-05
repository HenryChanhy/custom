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
                "apiKey":"6f55e36b",
                }
            ExData={
                "apiSecret":"adeaac8b252e4ed6a564cdcb1a064082",
                }
            param=func(data)
            param.update(SysData)
            url="http://IP+PORT/TrialCenter/order/Pampers/ST/"+arg["method"]
            #param["method"]=arg["method"]
            param["timestamp"]=GetTimeStamp()
            #param["timestamp"]="201512161115"
            paraList=[]
            for k,v in param.items():
#                if k=="appkey":
#                    continue
                if not str(v):
                    continue
                paraList.append(k+"="+str(v))

            for k,v in ExData.items():
                paraList.append(k+"="+str(v))

            paraList.sort(cmp)
            md5Str="&".join(paraList)
            md5Str=md5Str+"&apiSecret="+ExData["apiSecret"]
            #md5Str=ToUTF8Str(md5Str)
            param["sig"]=MD5Sign(md5Str)
            req=requests.post(url,param)

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
    result={}
    result["xmlValues"]=finalStr
    return result


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

if __name__=="__main__":
    test_main()
