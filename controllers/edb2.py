# -*- coding: utf-8 -*-
import xml.etree.ElementTree as XML_ET
import os
import time
import requests
import json
import hashlib
from datetime import datetime
import re

def cmp(x,y):
    x1=x.lower()
    y1=y.lower()
    if x1>y1:
        return 1
    if x1<y1:
        return -1
    return 0

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

def log_file(msg):
    dir=os.getcwd()
    fileName="err.txt"
    finalPath=os.path.join(dir,fileName)
    with open(finalPath,"ab") as f:
        f.write("[%s] %s\r\n"%(GetTimeStamp(),msg))
    return finalPath

def MD5Sign(md5Str):
    m=hashlib.md5()
    m.update(md5Str)
    return m.hexdigest().upper()

def TrialAPI(**arg):
    def _TrialAPI(func):
        def __TrialAPI(data):
            SysData={"apiKey":"57Hyjts8HHty",}
            ExData={"apiSecret":"iO7hbmH8-rbt6Hg_Yg6",}
            param=func(data)
            param.update(SysData)
            param.update(data)
            url="http://122.193.31.8:8080/TrialCenter/order/Pampers/ST/"+arg["method"]
            param["timestamp"]=str(int(time.time()))
            paraList=[]
            for k,v in param.items():
                if isinstance(v,str):
                    paraList.append(k+"="+str(v))
            paraList.sort(cmp)
            md5Str="&".join(paraList)
            md5Str=md5Str+ExData["apiSecret"]
            param["sig"]=MD5Sign(md5Str)
            log_file("%s %s"%(md5Str,param["sig"]))
            jsparam=json.dumps(param)
            req=requests.post(url,jsparam,verify=False)
            return json.loads(req.content)
        return __TrialAPI
    return _TrialAPI

@TrialAPI(method="updateOrderTrackingInfo")
def updateOTI(data):
    return {}

@TrialAPI(method="updateTrialOrderStatus")
def updateTOS(data):
    return {}
"""
@request.restful()
def onlyToEDB():
    response.view ='generic.'+request.extension  #return json
    def GET(*args,**vars):
        barcode_dict={'62015092412001':'6903148240014','62015092480001':'6903148238905',
                     '2015092412002':'6903148240021','2015092480002':'6903148238912',
                     '33320151016001':'6903148238912','33320151016002':'6903148238905'}
        keys=vars.keys()
        result={}
        if ('out_tid' in keys) and ('status' in keys) and ('appKey' in keys):
            if vars['appKey']=='updateandtos':
                a_row=db(db.trade.out_tid.like(vars['out_tid'])).select()
                if a_row:
                    a_row.first().update_record(status=vars['status'])
                    data={"order_id":vars['out_tid'],'status':vars['status']}
                    if vars['status']=='2':
                        data['message']=vars['msg']
                    else:
                        trade_content=a_row.as_list()[0]
                        if 'province' in trade_content.keys():
                            trade_content['privince']=trade_content['province']
                        for k,v in trade_content.items():
                            if isinstance(v,str):
                                trade_content[k]=v.decode('utf8')
                            if isinstance(v, datetime):
                                trade_content[k] = v.isoformat()
                        if trade_content['barCode'] in barcode_dict.keys():
                            trade_content['barCode']=barcode_dict[trade_content['barCode']]

                        if vars.has_key('hard_update'):
                            edbreturn=AddTrade(trade_content)
                            try:
                                a_row.first().update_record(edb_return=edbreturn['Success']['items']['item'][0]['is_success'])
                            except:
                                a_row.first().update_record(edb_return=edbreturn)
                            result['edb_return']=edbreturn
                        else:
                            if a_row.as_list()[0]['edb_return']==None or a_row.as_list()[0]['edb_return']!='True':
                                edbreturn=AddTrade(trade_content)
                                try:
                                    a_row.first().update_record(edb_return=edbreturn['Success']['items']['item'][0]['is_success'])
                                except:
                                    a_row.first().update_record(edb_return=edbreturn)
                                result['edb_return']=edbreturn
                    result['is_success']='t'
                else:
                    result['is_success']='o'
            else:
                result['is_success']='f'
        else:
            result['is_success']='f'
        return result
    return locals()
"""

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
            if not req.ok:
                print "requests FAIL"
                log_file("%s %s"%(arg,data))
                filePath=log_file(req.content)
                print "log_file in",filePath
                return
            return json.loads(req.content)
        return __EdbAPI
    return _EdbAPI

@EdbAPI(method="edbTradeAdd")
def AddTrade(data):
    orderTag=('out_tid','shop_id','storage_id','buyer_id','buyer_msg','buyer_email','buyer_alipay','seller_remark','consignee','address','postcode','telephone','mobilPhone','privince','city','area','actual_freight_get','actual_RP','ship_method','express','is_invoiceOpened','invoice_type','invoice_money','invoice_title','invoice_msg','order_type','process_status','pay_status','deliver_status','is_COD','serverCost_COD','order_totalMoney','product_totalMoney','pay_method','pay_commission','pay_score','return_score','favorable_money','alipay_transaction_no','out_payNo','out_express_method','out_order_status','order_date','pay_date','finish_date','plat_type','distributor_no','WuLiu','WuLiu_no','in_memo','other_remark','actual_freight_pay','ship_date_plan','deliver_date_plan','is_scorePay','is_needInvoice')
    productTag=('barCode','product_title','standard','out_price','favorite_money','orderGoods_Num','gift_Num','cost_Price','tid','product_stockout','is_Book','is_presell','is_Gift','avg_price','product_freight','shop_id','out_tid','out_productId','out_barCode','product_intro')
    orderXml=XML_ET.fromstring('<info><orderInfo></orderInfo></info>')
    productXml=XML_ET.fromstring('<product_info><product_item></product_item></product_info>')
    orderInfo=orderXml.find("orderInfo")
    itemInfo=productXml.find("product_item")
    for k,v in data.items():
        if k in orderTag:
            tmp=XML_ET.SubElement(orderInfo,k)
            tmp.text=v
        if k in productTag:
            tmp=XML_ET.SubElement(itemInfo,k)
            tmp.text=v
    orderInfo.append(productXml)
    finalStr=XML_ET.tostring(orderXml,"utf8")
    result={}
    result["xmlValues"]=finalStr[37:]
    return result

def test_main():
    data={
    "out_tid":"33",
    "shop_id":"127",
    "mobilPhone":"18565374663",
    #"storage_id":"38",
    "buyer_msg":"以前为左奇多圈而买包野食",
    #"postcode":"000000",
    "consignee":"冼俊华",
    "privince":"广东省",
    "city":"广州市",
    "area":"南沙区",
    "address":"广东省广州市南沙区东涌镇太",
    #"express":"EMS",
    #"invoice_msg":"121212",
    "order_date":"2016-08-18 11:47:33",
    "barCode":"BS6924743911659",
    "product_title":"奇多",
    "orderGoods_Num":'1'
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

if __name__=="__main__":
    test_main()
