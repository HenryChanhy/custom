__author__ = 'Administrator'
from simhash import Simhash,SimhashIndex
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

#@auth.requires_login()
@request.restful()
def TradeAdd():
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
        ('order_date' in keys)and\
        ('product_title' in vars['product_info'][0].keys())and \
        ('standard' in vars['product_info'][0].keys())and\
        ('out__tid' in vars['product_info'][0].keys()):
            ts=int(time.time())
            this_apiKey='A6BEA59B'
            this_apiSecret='1F6F088755B094DDAD3C7AEFEA73A1A1'
            essential_field=vars.keys()
            essential_field.sort()
            SigStr=""
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
                        SigStr=SigStr[0:len(SigStr)-1]
                        SigStr=SigStr+u"}"
                    SigStr=SigStr+u"]"+u"&"
                else:
                    SigStr=SigStr+unicode(field)+u"="+unicode(vars[field])+u"&"
            this_sig=MD5Sign((SigStr[0:len(SigStr)-1]+this_apiSecret).encode('utf8'))
            if (vars['sig']==this_sig) and (ts-int(vars['timestamp'])<180) and \
            ((vars['apiKey']).decode('unicode_escape')==(this_apiKey)):
                msg.append({'is_success':'true','response_Msg':u'成功导入系统'})
                content={}
                for field in essential_field:
                    if field =="sig" or field =="apiKey" or field=="timestamp":
                        continue
                    elif field=="product_info":
                        for f in vars["product_info"][0].keys():
                            content[f]=vars["product_info"][0][f]
                    else:
                        content[field]=vars[field]
                data={"order_id":'out_tid',"status": "0"}
                updateTOS(data)

                order_phone=db().select(db.trade.mobilPhone).as_list()
                if not {'mobilPhone':content['mobilPhone']} in order_phone:
                    data["status"]=1
                    db.trade.insert(**content)
                else:
                    data["status"]=2
                    data["messge"]=u"订单重复"
                updateTOS(data)
            else:
                msg.append({'is_success':'false','response_Msg':'wrong identifier params'})
        else:
            msg.append({'is_success':'false','response_Msg':'absence of essential field',})
        jsonObj['item']=msg
        return jsonObj
    return locals()


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

#@auth.requires_login()
@request.restful()
def GetEdbOrderInfo():
    response.view ='generic.'+request.extension  #return  json
    def GET(*args,**vars):
        keys=vars.keys()
        content={}
        if ('order_id' in keys)and('tracking_number' in keys) and\
        ('tracking_company' in keys):
            content['is_success']=True
            content.update(vars)
            order_info={
	        "order_id": vars['order_id'],
	        "tracking_number":vars['tracking_number'],
	        "tracking_company":vars['tracking_company']}
            updateOTI(order_info)
        else:
            content['is_success']=False
            content['wrong_reason']='absence of essential field'
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