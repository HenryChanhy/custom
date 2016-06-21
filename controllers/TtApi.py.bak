# -*- coding: utf-8 -*-
__author__ = 'Administrator'
import xml.etree.ElementTree as XML_ET
import os
import sys
import time
import hashlib
import chardet
import requests
import json
import openpyxl
from datetime import datetime
from time import mktime
#from snownlp import SnowNLP
import re
import redis
rds=redis.StrictRedis()
p=re.compile("[\.\!\|\,\\\$%^*+=\"\']+|[+！，。？、~@￥%……&*＠]+".decode("utf8"))
pspace=re.compile("\s+".decode("utf8"))
paddress=re.compile("-".decode("utf8"))
patt_keywd=re.compile("[号|楼|元|路|栋|区|室|园|组|道|村|幢|城|司|座|弄|店|期|巷|场|旁|寓|省|市|县|院|心|厦|门|口|集|镇|苑|层|街|景|居|舍|房|部|科|都|学|厂|方|后|属|面|下|户|收|处|内|向|队|馆|校|斜|社|所|商|站|局|行|庭|段|团]+".decode('utf8'))
zhixia=(u'北京',u'天津',u'上海',u'重庆')
zhixiashi=(u'北京市',u'天津市',u'上海市',u'重庆市')
zizhi=(u'内蒙古',u'西藏')
provinces=(u'河北',u'山西',u'辽宁',u'吉林',u'黑龙江',u'江苏',
    u'浙江',u'安徽',u'福建',u'江西',u'山东',u'河南',u'湖北',u'湖南',u'广东',
    u'海南',u'四川',u'贵州',u'云南',u'陕西',u'甘肃',u'青海')
provincesf=(u'北京',u'上海',u'天津',u'重庆',u'香港',u'澳门',u'河北省',u'山西省',u'辽宁省',u'吉林省',u'黑龙江省',u'江苏省',
    u'浙江省',u'安徽省',u'福建省',u'江西省',u'山东省',u'河南省',u'湖北省',u'湖南省',u'广东省',u'广西壮族自治区',
    u'海南省',u'四川省',u'贵州省',u'云南省',u'西藏自治区',u'陕西省',u'甘肃省',u'青海省',u'宁夏回族自治区',u"新疆维吾尔自治区",u'内蒙古自治区')
fuzzywords=(u'省',u'市',u'县',u'镇',u'工业区',u'业园区',u'工贸园',u'公园',u'管理区',u'开发区',u'新区',u'大道',u'国道',u'广场',u'街道',
            u'道',u'路',u'桥',u'路口',u'街上',u'街',u'街上',u'道上',u'道口',u'门口',u'市场',u'附近',u'车站',u'快递',
            u'圆通',u'顺丰',u'中通',u'申通',u'韵达',u'汇通',u'邮局',u'邮政局',u'网点',u'速递',u'镇邮局',u'物流',
            u'桥头',u'交叉口',u'三岔口',u'交口',u'乡', u'旗',u'球场',u'快递公司',u'快递点',u'快递处',u'收点')
fuzzywords1=(u'自取',u'自提',u'取件', u'站', u'营业点', u'电话', u'短信', u'电联', u'打电话', u'点', u'中转站', )
fixaddress={u"其它区":u"",u"市辖区":u"",u"地址":u"",u"墉桥区":u"埇桥区",u"璧山区":u"璧山县",u"高陵区":u"高陵县",u"富阳区":u"富阳市",
            u"藁城区":u"藁城市",u"溧水区":u"溧水县",u"南溪区":u"南溪县",u"鹿泉区":u"鹿泉市",u"大足区":u"大足县",
            u"毕节市":u"七星关区",u"铜仁市":u"铜仁地区",u"浑南新区":u"浑南区",u"东陵区":u"浑南区",u"赣榆区":u"赣榆县",
            u"铜梁区":u"铜梁县",u"龙马潭":u"龙马潭区",u"上虞区":u"上虞市",u"广州省":u"广东省",u"广西省":u"",u"临河市":u"临河区",
            u"娄底地区":u"娄底市",u"海东市":u"海东地区",u"菏泽地区":u"菏泽市",u"巴彦淖尔盟":u"巴彦淖尔市",u"+":u"＋",
            u"望城区":u"望城县",u"增城区":u"增城市",u"溧水区":u"溧水县",u"江都区":u"江都市",u"清新区":u"清新县",
            u"文山市":u"文山县",u"从化区":u"从化市",u"潮安区":u"潮安县",u"电白区":u"电白县",u"藁城区":u"藁城市",u"陵城区":u"陵县",
            u"南康区":u"南康市",u"綦江区":u"綦江县",u"增城区":u"增城市",u"吴江区":u"吴江市",u"铜山区":u"铜山县",u"文登区":u"文登市",
            u"杨凌区":u"杨陵区",u"长安县":u"长安区",u"颖州区":u"颍州区"}

def findprovincebycity(straddr):
    strcity=straddr+u"市"
    if rds.hexists('dictcity',straddr):
        return getprovince(rds.hget('dictcity',straddr).decode('utf8'))
    elif rds.hexists('dictcity',strcity):
        return getprovince(rds.hget('dictcity',strcity).decode('utf8'))
    else:
        return u""

def getprovince(straddr):
    if straddr in provinces:
        result=straddr+u"省"
    elif straddr in provincesf:
        result=straddr
    elif straddr in zhixia:
        result=straddr
    elif straddr in zhixiashi:
        result=straddr[:2]
    elif straddr in zizhi:
        result=straddr+u"自治区"
    elif straddr.startswith(u"广西"):
        result=u"广西壮族自治区"
    elif straddr.startswith(u"宁夏"):
        result=u"宁夏回族自治区"
    elif straddr.startswith(u"新疆"):
        result=u"新疆维吾尔自治区"
    else:
        result=u""
    return result

def getcity(straddr):
    addr=straddr+u"市"
    if straddr == u"毕节市" or straddr == u"毕节":
        return u"毕节地区"
    elif straddr == u"铜仁市" or straddr == u"铜仁":
        return u"铜仁地区"
    elif straddr == u"市辖区" or straddr ==u"县" or straddr.endswith(u"直辖县级行政区划"):
        return u""
    elif rds.sismember('citys',straddr):
        return straddr
    elif rds.sismember('citys',addr):
        return straddr +u"市"
    else:
        return u""

#查区信息
def getarea(straddrfilter):
    straddr=filterotherarea(straddrfilter)
    if rds.sismember('areas',straddr):
        return straddr
    elif rds.sismember('areas',straddr + u"市"):
        return straddr + u"市"
    elif rds.sismember('areas',straddr + u"区"):
        return straddr + u"区"
    elif rds.sismember('areas',straddr + u"县"):
        return straddr + u"县"
    else:
        return u""

#用省,区 查市
def getcitybyProvArea(prov,straddr):
    #comkey=prov+getarea(straddr)
    comkey=prov+straddr
    if rds.hexists('PCA',comkey):
        return rds.hget('PCA',comkey).decode('utf8')
    else:
        return u""

def getcityclass(city,area):
    if rds.hexists('areaclass',area):
        return rds.hget('areaclass',area).decode('utf8')
    elif rds.hexists('cityclass',city):
        return rds.hget('cityclass',city).decode('utf8')
    else:
        return u""

def findstreetincity(city,straddr):
    if rds.exists(city):
        streets=rds.smembers(city)
        for s in streets:
            su=s.decode('utf8')
            if su in straddr:
                return su
    return ""

#从字符串开始 去重1次
def filterdupaddress(straddr):
    dup=0
    for dup in range(len(straddr)/2,0,-1):
        if dup > 3:
            if straddr[:dup] in straddr[dup:]:
                break
        else:
            if straddr[:dup] in straddr[dup:dup+len(straddr[:dup])]:
                break
    if dup > 1:
        dupsplit=straddr.rsplit(straddr[:dup],1)
        return dupsplit[0]+dupsplit[1]
    else:
        return straddr

def getkeywd(straddr):
    result=[]
    keypos=[]
    keywd=patt_keywd.findall(straddr)
    for i in range(0,len(straddr)):
        if straddr[i:i+1] in keywd:
            keypos.append(i)
    j=0
    for k in keypos:
        result.append(straddr[j:k+1])
        j=k+1
    if j<len(straddr):
        result.append(straddr[j:])
    return result

#根据分词去重
def dynareduce(address):
    if len(address)>0:
        #addwords=SnowNLP(address).words
        addwords=getkeywd(address)
        for pos in range(0,len(addwords)-1):
            for pos1 in range(pos+1,len(addwords)-1):
                if len(addwords[pos]) >1 and addwords[pos] == addwords[pos1] and not addwords[pos].isdigit():
                    addwords[pos1]=u""
                    break
        result=u""
        for words in addwords:
            result+=words
        return filterdupaddress(result)
    else:
        return address

#根据省市区详细地址 重构详细地址.
def setdetail(prov,city,area,detail):
    baredetail=detail.replace(area,u"").replace(city,u"").replace(prov,u"")
    if prov in zhixia:
        return city+area+baredetail
    elif city==area:
        return prov+city+baredetail
    else:
        return prov+city+area+baredetail

#纠正区域信息
def filterotherarea(straddr):
    for fixword in fixaddress.keys():
        if fixword in straddr:
            return straddr.replace(fixword,fixaddress[fixword])
    return straddr

bknm=rds.smembers('blackname')
def isbknm(straddr):
    for i in bknm:
        if i.decode('utf8') in straddr:
            return True
    return False

may_bknm=rds.smembers('may_blackname')
def is_may_blackname(straddr):
    for i in may_bknm:
        if i.decode('utf8') in straddr:
            return True
    return False

#是否模糊字结尾
def isfuzzyend(straddr):
    for i in fuzzywords:
        if straddr.endswith(i):
            return True
    return False

def isfuzzyend1(straddr):
    for i in fuzzywords1:
        if straddr.endswith(i):
            return True
    return False

def procaddress(**content):
    addr=""
    city=""
    area=""
    fulladdr=u""
    content['addrbkp']=content["address"]
    Detailaddress=pspace.sub("",content["address"])
    if not content.has_key("status"):
        content["status"]=u""
    if not content.has_key("area"):
        content["area"]=u""
    if not content.has_key("city"):
        content["city"]=u""
    if not content.has_key("province"):
        content["province"]=u""
    if content["province"]==u"-":
        content["province"]=u""
        content["city"]=u""
        content["area"]=u""
        Detailaddress=paddress.sub("",content["address"])
    else:
        if Detailaddress.startswith(content["province"]):
            Detailaddress=Detailaddress.replace(content["province"],"",1)
        if Detailaddress.startswith(content["city"]):
            Detailaddress=Detailaddress.replace(content["city"],"",1)
        if Detailaddress.startswith(content["area"]):
            Detailaddress=Detailaddress.replace(content["area"],"",1)
    content["address"]=Detailaddress
    if content["province"]!='':
        addr=getprovince(content["province"])
        if addr:
            content["province"]=addr
        #else:
            #content["province"]=u""
    if content["city"]!='':
        city=getcity(content["city"])
        if city!="":
            content["city"]=city
    if content["area"]!='': #有详细地址字段
        area=getarea(content["area"])
        if area!="":
            content["area"]=area
    if addr!="" and city!="" and area!="":
        content["province"]=addr
        content["city"]=city
        content["area"]=area
        if content["address"].startswith(addr) and city in content["address"] and area in content["address"]:
            fulladdr=content["address"]
        elif area in content["address"] and city in content["address"]:
            fulladdr=addr+content["address"]
        elif area in content["address"]:
            fulladdr=addr+area+content["address"]
        else:
            if addr in zhixia:
                fulladdr=city+area+content["address"]
            else:
                fulladdr=addr+city+area+content["address"]
        content["address"]=dynareduce(filterotherarea(fulladdr))
        area=getarea(area)
        if city == u"":
            if addr in zhixia:
                city=addr+u"市"
            else:
                city = area
            content["city"]=city
        else:
            content["city"]=city
    else:#没有省市区字段，需拆分详细地址
        if addr!="":
            fulladdr+=addr
        if city!="":
            fulladdr+=city
        if area!="":
            fulladdr+=area
        fulladdr+=content["address"]
        content["address"]=filterotherarea(fulladdr)
        posp=0
        posc=0
        posa=0
        addrs=getkeywd(fulladdr)
        if addr=="":
            addr=getprovince(content["province"])
        if addr=="":
            addr=findprovincebycity(content["city"])
        if addr=="":
            for posp in range(0,len(addrs)-1):
                addr=getprovince(addrs[posp])
                if addr!="":
                    break
        if addr=="":
            for posp in range(0,len(addrs)-1):
                addr=findprovincebycity(addrs[posp])
                if addr!="":
                    break
        if addr=="":
            addr=u""
            content["status"]="0" #找不到省信息
        else :
            if addr in zhixia:
                content["address"]=u""
            else:
                content["address"]=addr
            if city=="" and content["city"]!=u"":
                city=getcity(content["city"])
            if city=="" and content["area"]!=u"":
                city=getcity(content["area"])
            if city=="" and content["city"]!=u"":
                city=getcitybyProvArea(addr,content["city"])
                if city!="":
                    area=getarea(content["city"])
            if city=="" and content["area"]!=u"":
                city=getcitybyProvArea(addr,content["area"])
                if city!="":
                    area=getarea(content["area"])
            if city=="":
                for posc in range(posp,len(addrs)-1):
                    city=getcity(addrs[posc])
                    if city!="":
                        break
                    city=getcitybyProvArea(addr,addrs[posc])
                    if city!="":
                        area=getarea(addrs[posc])
                        break
            if city=="" or findprovincebycity(city)!=addr:
                city=u""
                content["status"]="6" #找不到市信息
            else:
                content["address"]+=city
            if area =="" and content["area"]!=u"":
                area=getarea(content["area"])
            if area=="":
                for posa in range(posc,len(addrs)-1):
                    area=getarea(addrs[posa])
                    if area!="":
                        break
            if area==u"" or getcitybyProvArea(addr,area)!= city:
                area=u""
                posa=1
                content["status"]+="8"#找不到区信息
            else:
                content["address"]+=area
                if city==u"":
                    city=area
            for detail in addrs[posa:]:
                content["address"]+=detail
        content["province"]=addr
        content["city"]=city
        content["area"]=area
        content["address"]=dynareduce(filterotherarea(content["address"]))
    content["address"]=setdetail(content["province"],content["city"],content["area"],content["address"])
    if isfuzzyend(content["address"]) or u'测试' in content["address"]:
        content["status"]="2"
        content["wrong_reason"]=u"不通过"
    elif isbknm(content["address"]):
        content["status"]="2"
        content["wrong_reason"]=u"黑名单"
    elif is_may_blackname(content["address"]):
        content["status"] +="9"
    elif isfuzzyend1(content["address"]):
        content["status"] += "4" #待查看
    street=findstreetincity(content["city"],content["address"])
    if street!="":
        content["other_remark"]=street
        content["address"]=content["address"].replace(street,u"")
    content['city_class']=getcityclass(content["city"],content["area"])
    if not content["status"]:
        content["status"]="55"
    return content

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

@request.restful()
def test_TOS():
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
                    if a_row[0]['oti_return']==1:
                        result['is_success']='t'
                    else:
                        a_row.first().update_record(status=vars['status'])
                        data={"order_id":vars['out_tid'],'status':vars['status']}
                        if vars['status']=='2':
                            data['message']=vars['msg']
                            a_row.first().update_record(wrong_reason=vars['msg'])
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
                            trade_content['out_tid']='TC'+trade_content['out_tid']
                            if a_row.as_list()[0]['edb_return']==None or a_row.as_list()[0]['edb_return']!='True':
                                edbreturn=AddTrade(trade_content)
                                try:
                                    a_row.first().update_record(edb_return=edbreturn['Success']['items']['item'][0]['is_success'])
                                except:
                                    a_row.first().update_record(edb_return=edbreturn)
                                result['edb_return']=edbreturn
                        if a_row.as_list()[0]['tc_return']==None or a_row.as_list()[0]['tc_return']!='true':
                            ctreturn=updateTOS(data)
                            a_row.first().update_record(tc_return=ctreturn['result'])
                            result['CT_return']=ctreturn
                        result['is_success']='t'
                else:
                    result['is_success']='o'
            else:
                result['is_success']='f'
        else:
            result['is_success']='f'
        return result
    return locals()
    '''wb=openpyxl.load_workbook('/home/20160121_27源数据60658条.xlsx')
    wst= wb.get_sheet_by_name(name = 'true')
    wsw= wb.get_sheet_by_name(name = 'wrong')
    for i in range(2,wst.max_row+1):
        outtid=wst.cell(row=i,column=3).value.encode('utf8')
        data={"order_id":outtid}
        data["status"]="3"
        result=updateTOS(data)
        log_file("%s %s"%(data,result))
        db(db.trade.out_tid==wst.cell(row=i,column=3).value).select().first().update_record(status=3)
    for i in range(2,wsw.max_row+1):
        outtid=wsw.cell(row=i,column=3).value.encode('utf8')
        data={"order_id":outtid}
        data["status"]="2"
        data["message"]=wsw.cell(row=i,column=17).value.encode('utf8')
        result=updateTOS(data)
        log_file("%s %s"%(data,result))
        db(db.trade.out_tid==wsw.cell(row=i,column=3).value).select().first().update_record(status=2)'''


@request.restful()
def testredis():
    response.view ='generic.'+request.extension  #return json
    def GET(*args,**vars):
        result=procaddress(**vars)
        return result
    return locals()

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

#测试用，可删除
def test_OTI():
    orderinfo={
	"order_id": "8444",
	"tracking_number": "3100901633843",
	"tracking_company": "17"
    }
    result=updateOTI(orderinfo)
    log_file("%s %s"%(orderinfo,result))

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

def test_2edb():
    wb=openpyxl.load_workbook('/home/trade20160125h_36（100条测试71条合格）.xlsx')
    wst= wb.get_sheet_by_name(name = 'true71')
    results=[]
    for i in range(2,wst.max_row+1):
        outtid=wst.cell(row=i,column=28).value.encode('utf8')
        trade_content=db(db.trade.out_tid==wst.cell(row=i,column=28).value).select().first()
        for k,v in trade_content.items():
            if isinstance(v,str):
                trade_content[k]=v.decode('utf8')
            if isinstance(v, datetime):
                trade_content[k] = v.isoformat()
    result=AddTrade(trade_content)
    return result

#{'bar_code':vars['product_info'][0]['barCode']} in AllBarcode
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
            edbdata={}
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
                            edbdata[j]=d[j]
                        SigStr=SigStr[0:len(SigStr)-1]
                        SigStr=SigStr+u"}"
                    SigStr=SigStr+u"]"+u"&"
                else:
                    SigStr=SigStr+unicode(field)+u"="+unicode(vars[field])+u"&"
                    if (field != 'apiKey') and (field !='timestamp'):
                        edbdata[field]=vars[field]
            edbdata['address']=edbdata['address'].replace('\r','')
            edbdata['address']=edbdata['address'].replace(',','-')
            if ('province' in keys):
                edbdata['province']=edbdata['province'].replace('\r','')
                edbdata['province']=edbdata['province'].replace(',','-')
            if  ('city' in keys):
                edbdata['city']=edbdata['city'].replace('\r','')
                edbdata['city']=edbdata['city'].replace(',','-')
            if  ('area' in keys):
                edbdata['area']=edbdata['area'].replace('\r','')
                edbdata['area']=edbdata['area'].replace(',','-')
            if ('consignee' in keys):
                edbdata['consignee']=edbdata['consignee'].replace('\r','')
                edbdata['consignee']=edbdata['consignee'].replace(',','-')
            if ('plat_type' in keys):
                if edbdata['plat_type']==None :
                    edbdata['plat_type']='TrialCenter'
            this_sig=MD5Sign((SigStr[0:len(SigStr)-1]+this_apiSecret).encode('utf8'))
            #AllBarcode=db().select(db.AllBarcode.bar_code).as_list()
            if (vars['sig']==this_sig) and (ts-int(vars['timestamp'])<180) and \
            ((vars['apiKey']).decode('unicode_escape')==(this_apiKey)):
                #getorderid=db.trade.update_or_insert(db.trade.out_tid==edbdata['out_tid'],**edbdata)
                t=db(db.trade.out_tid==edbdata['out_tid']).select()
                edbdata=procaddress(**edbdata)
                if t:
                    msg.append({'is_success':'true','response_Msg':'duplicate trade'})
                    t.first().update_record(**edbdata)
                else:
                    tcpid=db.trade.insert(**edbdata)
                    if tcpid:
                        msg.append({'is_success':'true','response_Msg':'import to TaoTongGroup successfully'})
                    else:
                        msg.append({'is_success':'false','response_Msg':'unexpected data'})
            else:
                msg.append({'is_success':'false','response_Msg':'wrong verification'})
        else:
            msg.append({'is_success':'false','response_Msg':'absence of essential field'})
        jsonObj['item']=msg
        return jsonObj
    return locals()

#@auth.requires_login()
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
            trade_exist=db(db.trade.out_tid.like(order_info['orderId'])).select()
            if not order_info['orderId'].startswith('TT'):
                if trade_exist:
                    WuLiu_info={"order_id": order_info['orderId'],
	                "tracking_number":order_info['trackingNo']}
                    if order_info['logisticCompany'] in WuLiu_dict.keys():
                        WuLiu_info["tracking_company"]=str(WuLiu_dict[order_info['logisticCompany']])
                        result=updateOTI(WuLiu_info)
                        if result['result']=='true':
                            content['isSuccess']=True
                            content['errorCode']=1
                            content['errorMsg']='处理成功'
                        else:
                            if result['error']=='1032':
                                content['isSuccess']=True
                                content['errorCode']=1
                                content['errorMsg']='处理成功'
                            else:
                                content['isSuccess']=False
                                content['errorCode']=2
                                content['errorMsg']='订单不存在'
                    else:
                        content['isSuccess']=False
                        content['errorCode']=5
                        content['errorMsg']='物流公司不存在'
                    trade_exist.first().update_record(oti_return=content['errorCode'])
                else:
                    content['isSuccess']=True
                    content['errorCode']=1
                    content['errorMsg']='处理成功'
            else:
                content['isSuccess']=True
                content['errorCode']=1
                content['errorMsg']='处理成功'
        else:
            content['isSuccess']=False
            content['errorCode']=9
            content['wrong_reason']='订单号格式错误'
        return content
    return locals()

#@auth.requires_login()
#@request.restful()
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

#@request.restful()
def TradeUpdate():
    response.view ='generic.'+request.extension  #return  json
    def PUT(table_name,record_id,**vars):
        return db(db[table_name].order_id==record_id).update(**vars)
    return locals()

#@request.restful()
def TradeDelete():
    response.view ='generic.'+request.extension  #return  json
    def DELETE(table_name,record_id):
        return db(db[table_name].order_id==record_id).delete()
    return locals()

if __name__=="__main__":
    test_TOS()
