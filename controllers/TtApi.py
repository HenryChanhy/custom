__author__ = 'Administrator'
#from simhash import Simhash,SimhashIndex
import xml.etree.ElementTree as XML_ET
import os
import sys
import time
import hashlib
import chardet
import requests
import json

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
            SysData={"apiKey":"qhT49hGFv5rks",}
            ExData={"apiSecret":"wh76BtGfks7fVbkiu",}
            param=func(data)
            param.update(SysData)
            param.update(data)
            #url="http://nwct.biz:18910/TrialCenter/order/Pampers/ST/"+arg["method"]
            url="http://122.193.31.5:8080/TrialCenter/order/Pampers/ST/"+arg["method"]
            param["timestamp"]=str(int(time.time()))
            paraList=[]
            for k,v in param.items():
                if isinstance(v,str):
                    paraList.append(k+"="+str(v))
            paraList.sort(cmp)
            md5Str="&".join(paraList)
            md5Str=md5Str+ExData["apiSecret"]
            param["sig"]=MD5Sign(md5Str)
            jsparam=json.dumps(param)
            req=requests.post(url,jsparam,verify=False)
            JsonObj=json.loads(req.content)
            return JsonObj
        return __TrialAPI
    return _TrialAPI

@TrialAPI(method="updateOrderTrackingInfo")
def updateOTI(data):
    return {}

@TrialAPI(method="updateTrialOrderStatus")
def updateTOS(data):
    return {}

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

#@EdbAPI(method="edbTradeAdd")
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
            tmp.text=v.decode('utf8')
        if k in productTag:
            tmp=XML_ET.SubElement(itemInfo,k)
            tmp.text=v.decode('utf8')
    orderInfo.append(productXml)
    finalStr=XML_ET.tostring(orderXml,"utf8")
    result={}
    print finalStr
    result["xmlValues"]=finalStr[37:]
    return result

#@auth.requires_login()
@request.restful()
def AddTradeToEdb():
    response.view ='generic.'+request.extension  #return  json
    def POST(tablename,**vars):
        msg=[]
        jsonObj={}
        keys=vars.keys()
        for k in keys:
            k.decode('unicode_escape')
        if ('apiKey' in keys)and('product_info' in keys)and\
        ('timestamp' in keys)and('sig' in keys) and\
        ('out_tid' in keys)and ('shop_id' in keys)and\
        ('consignee' in keys)and('address' in keys)and\
        ('postcode' in keys)and('mobilPhone' in keys)and\
        ('order_date' in keys)and('storage_id' in keys)and\
        ('barCode' in vars['product_info'][0].keys())and \
        ('product_title' in vars['product_info'][0].keys())and \
        ('standard' in vars['product_info'][0].keys())and\
        ('out__tid' in vars['product_info'][0].keys()):
            ts=int(time.time())
            this_apiKey='A6BEA59B'
            this_apiSecret='1F6F088755B094DDAD3C7AEFEA73A1A1'
            essential_field=vars.keys()
            essential_field.sort()
            SigStr=""
            orderdata={}
            for field in essential_field:
                if field =="sig" or field =="apiSecret":
                    continue
                elif field =="product_info":
                    SigStr=SigStr+unicode(field)+u"="+u"["
                    for d in vars["product_info"]:
                        k=d.keys()
                        k.sort()
                        SigStr=SigStr+u"{"
                        for j in k:
                            SigStr=SigStr+unicode(j)+u"="+unicode(d[j])+u"&"
                            orderdata[j]=d[j]
                        SigStr=SigStr[0:len(SigStr)-1]
                        SigStr=SigStr+u"}"
                    SigStr=SigStr+u"]"+u"&"
                elif field =="apiKey" or field =="timeStamp":
                    SigStr=SigStr+unicode(field)+u"="+unicode(vars[field])+u"&"
                else:
                    SigStr=SigStr+unicode(field)+u"="+unicode(vars[field])+u"&"
                    orderdata[field]=vars[field]
            this_sig=MD5Sign((SigStr[0:len(SigStr)-1]+this_apiSecret).encode('utf8'))

            if (vars['sig']==this_sig) and (ts-int(vars['timestamp'])<180) and \
            ((vars['apiKey']).decode('unicode_escape')==(this_apiKey)):
                msg.append({'is_success':'true','response_Msg':'import to TaoTongGroup successfully'})
            else:
                msg.append({'is_success':'false','response_Msg':'wrong identifier params sig or barCode'})
        else:
            msg.append({'is_success':'false','response_Msg':'absence of essential field',})
        jsonObj['item']=msg
        return jsonObj
    return locals()

@request.restful()
def GetEdbOrderInfo():
    WuLiu_dict={}
    response.view ='generic.'+request.extension
    def GET(*args,**vars):
        keys=vars.keys()
        content={}
        if ('orderId' in keys)and('status' in keys) and\
('logisticCompany' in keys)and('trackingNo' in keys) and\
('updateTime' in keys)and('app_key' in keys):
            WuLiu_dict={
'EMS':'1','HTKY':'10','ZJS':'11','STO':'12','ZDY':'13','ZDY':'14','YUNDA':'15',
'FEDEX':'16','DBL':'17','RFD':'18','ZT':'19','STO':'2','POSTB':'20','SF':'6',
'STO':'21','OTHER':'22','OTHER':'23','UC':'24','FAST':'25','STO':'26','SF':'7',
'TTKDEX':'27','SF':'28','SF':'29','EMS':'3','ZTO':'30','STO':'31','YUNDA':'32',
'SF':'33','SF':'34','YUNDA':'35','YTO':'36','TTKDEX':'37','YTO':'4','TTKDEX':'5',
'YUNDA':'8','ZTO':'9'}
            order_info={}
            for k,v in vars.items():
                if k=='app_key':
                    continue
                elif k=='status':
                    order_info['order_status']=v
                elif k=='orderId':
                    order_info['orderId']=v.replace('TC','')
                else:
                    order_info[k]=v
            db.WuLiuInfo.update_or_insert(db.WuLiuInfo.orderId==order_info['orderId'],**order_info)
            if db(db.trade.out_tid.like(order_info['orderId'])).select():
                WuLiu_info={"order_id": order_info['orderId'],
	            "tracking_number":order_info['trackingNo']}
                if order_info['logisticCompany'] in WuLiu_dict.keys():
                    WuLiu_info["tracking_company"]=str(WuLiu_dict[order_info['logisticCompany']])
                    result=updateOTI(WuLiu_info)
                    if result['result']=='true':
                        content['isSuccess']=True
                        content['errorCode']=1
                        content['errorMsg']='����ɹ�'
                    else:
                        if result['error']=='1032':
                            content['isSuccess']=True
                            content['errorCode']=1
                            content['errorMsg']='����ɹ�'
                        else:
                            content['isSuccess']=False
                            content['errorCode']=2
                            content['errorMsg']='����������'
                else:
                    content['isSuccess']=False
                    content['errorCode']=5
                    content['errorMsg']='������˾������'
            else:
                content['isSuccess']=False
                content['errorCode']=2
                content['errorMsg']='�����Ų�����'
        else:
            content['isSuccess']=False
            content['errorCode']=9
            content['wrong_reason']='�����Ÿ�ʽ����'
        return content
    return locals()

#@auth.requires_login()
@request.restful()
def TradeGet():
    response.view ='generic.'+request.extension  #return  json
    def GET(*args,**vars):
        patterns=[
            "/products[db_map]",
            "/productid/{db_map.id}",
            "/product_exid/{db_map.field_order}",
            "/product/{custom_order.user_name.startswith}",
            "/product/{custom_order.user_name}/:field",
            "/trades[trade]",
            "/tradeTid/{trade.tid}",
            "/tradeOut/{trade.out_tid}"
        ]
        #patterns = 'auto'
        parser = db.parse_as_rest(patterns,args,vars)
        if parser.status == 200:
            return dict(content=parser.response)
        else:
            raise HTTP(parser.status,parser.error)
    return locals()

@request.restful()
def TradeUpdate():
    response.view ='generic.'+request.extension  #return  json
    def PUT(table_name,record_id,**vars):
        return db(db[table_name].order_id==record_id).update(**vars)
    return locals()

@request.restful()
def TradeDelete():
    response.view ='generic.'+request.extension  #return  json
    def DELETE(table_name,record_id):
        return db(db[table_name].order_id==record_id).delete()
    return locals()

if __name__=="__main__":
    data0={
    "actual_freight_get": "1",
    "actual_freight_pay": "1",
    "actual_RP": "1",
    "address": "\\u0038\\u0063",
    "alipay_transaction_no": "1",
    "apiKey": "A6BEA59B",
    "area": "\\u9759\\u5B89\\u533A",
    "buyer_alipay": "1",
    "buyer_email": "398282040@qq.com",
    "buyer_id": "1",
    "buyer_msg": "",
    "city": "\\u4E0A\\u6D77\\u5E02",
    "consignee": "\\u007A\\u006B",
    "deliver_date_plan": "1",
    "deliver_status": "1",
    "distributor_no": "1",
    "express": "1",
    "favorable_money": "1",
    "finish_date": "2016-07-2110:57:31",
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
    "order_date": "2016-07-2110:57:31",
    "order_totalMoney": "1",
    "order_type": "1",
    "other_remark": "1111111",
    "out_express_method": "1",
    "out_order_status": "1",
    "out_payNo": "1",
    "out_tid": "bsg32",
    "pay_commission": "1",
    "pay_date": "2016-07-2110:57:31",
    "pay_method": "1",
    "pay_score": "1",
    "pay_status": "1",
    "plat_type": "1",
    "postcode": "201203",
    "process_status": "1",
    "product_info": [{
            "avg_price": "",
            "barCode": "1",
            "cost_Price": "2.00",
            "favorite_money": "2.00",
            "gift_Num": "0",
            "is_Book": "0",
            "is_Gift": "0",
            "is_presell": "0",
            "orderGoods_Num": "1",
            "out__tid": "bsg32",
            "out_barCode": "1",
            "out_price": "2.00",
            "out_productId": "1",
            "product_freight": "0.00",
            "product_intro": "testproductintro",
            "product_stockout": "0",
            "product_title": "\\u6842\\u683C\\u9187\\u9999\\u0035\\u0034\\u0030\\u0067\\u002A\\u0033\\uFF08\\u725B\\u5976\\u9AD8\\u9499\\u002B\\u7EA2\\u67A3\\u9AD8\\u94C1\\u002B\\u7D2B\\u85AF\\u9AD8\\u7EA4\\uFF09",
            "shop__id": "125",
            "standard": "\\u6842\\u683C\\u9187\\u9999\\u0035\\u0034\\u0030\\u0067\\u002A\\u0033\\uFF08\\u725B\\u5976\\u9AD8\\u9499\\u002B\\u7EA2\\u67A3\\u9AD8\\u94C1\\u002B\\u7D2B\\u85AF\\u9AD8\\u7EA4\\uFF09",
            "t_id": "B16072110573189"
        }, {
            "avg_price": "",
            "barCode": "5",
            "cost_Price": "2.00",
            "favorite_money": "2.00",
            "gift_Num": "0",
            "is_Book": "0",
            "is_Gift": "0",
            "is_presell": "0",
            "orderGoods_Num": "1",
            "out__tid": "bsg32",
            "out_barCode": "5",
            "out_price": "2.00",
            "out_productId": "5",
            "product_freight": "0.00",
            "product_intro": "testproductintro",
            "product_stockout": "0",
            "product_title": "\\u6842\\u683C\\u9AD8\\u7EA4\\u71D5\\u9EA6\\u4E73\\u0032\\u0035\\u0030\\u006D\\u006C\\u002A\\u0036\\u002A\\u0033\\uFF08\\u9999\\u8549\\u002B\\u539F\\u5473\\u002B\\u699B\\u679C\\uFF09",
            "shop__id": "125",
            "standard": "\\u6842\\u683C\\u9AD8\\u7EA4\\u71D5\\u9EA6\\u4E73\\u0032\\u0035\\u0030\\u006D\\u006C\\u002A\\u0036\\u002A\\u0033\\uFF08\\u9999\\u8549\\u002B\\u539F\\u5473\\u002B\\u699B\\u679C\\uFF09",
            "t_id": "B16072110573189"
        }],
    "product_totalMoney": "1",
    "province": "\\u4E0A\\u6D77",
    "return_score": "1",
    "seller_remark": "11111",
    "serverCost_COD": "1",
    "ship_date_plan": "1",
    "ship_method": "1",
    "shop_id": "125",
    "sig": "",
    "storage_id": "24",
    "telephone": "1",
    "tid": "1",
    "timestamp": 1468477769,
    "WuLiu": "1",
    "WuLiu_no": "1"}
    AddTrade(data0)

















