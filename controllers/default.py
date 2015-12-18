# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
#
#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
####rowcontent['mobile'] in db().select(db.history_order.mobile)#########
# #######################################################################
import re
from simhash import Simhash,SimhashIndex
from gluon.http import redirect
import openpyxl
#from plugin_sqleditable.editable import SQLEDITABLE
auth.settings.allow_basic_login = True
auth.define_tables(username=True)
#SQLEDITABLE.init()

provinces=(u'北京',u'天津',u'河北',u'山西',u'内蒙古',u'辽宁',u'吉林',u'黑龙江',u'上海',u'江苏',
           u'浙江',u'安徽',u'福建',u'江西',u'山东',u'河南',u'湖北',u'湖南',u'广东',u'广西',
           u'海南',u'重庆',u'四川',u'贵州',u'云南',u'西藏',u'陕西',u'甘肃',u'青海',u'宁夏',
           u'新疆',u'香港',u'澳门',u'台湾')
zhixia=(u'北京',u'天津',u'重庆',u'上海')
texing=(u'香港',u'澳门')
SKU_dict={u'589203710279202':u'18片S码',
u'690314820783301':u'18片NB码',
u'589203710279204':u'8片S码',
u'690314820785503':u'8片NB码'}
top4_city=(u'北京市',u'成都市',u'广州市',u'上海市')
A_city=(u'合肥市',u'福州市',u'兰州市',u'深圳市','南宁市',u'贵阳市',u'海口市',u'石家庄市',
u'郑州市',u'哈尔滨市',u'武汉市',u'长沙市',u'南京市',u'大连市',u'沈阳市',u'呼和浩特市',
u'银川市',u'西宁市',u'济南市',u'青岛市',u'太原市',u'西安市',u'天津市',u'拉萨市',u'昆明市',
u'杭州市',u'重庆市')

def check_order():
    orderList=db(db.wrong_order).select().as_list()
    return locals()

def init_db():
    db.db_map.insert(table_type='excel',table_name='custom_order',field_name=u'订单编号',field_id='order_id',field_order=1)
    db.db_map.insert(table_type='excel',table_name='custom_order',field_name=u'店铺名称',field_id='shop_name',field_order=2)
    db.db_map.insert(table_type='excel',table_name='custom_order',field_name=u'外部平台单号',field_id='ex_id',field_order=3)
    db.db_map.insert(table_type='excel',table_name='custom_order',field_name=u'电话',field_id='telephone',field_order=4)
    db.db_map.insert(table_type='excel',table_name='custom_order',field_name=u'手机',field_id='mobile',field_order=5)
    db.db_map.insert(table_type='excel',table_name='custom_order',field_name=u'收货人',field_id='user_name',field_order=6)
    db.db_map.insert(table_type='excel',table_name='custom_order',field_name=u'收货省',field_id='province',field_order=7)
    db.db_map.insert(table_type='excel',table_name='custom_order',field_name=u'收货市',field_id='city',field_order=8)
    db.db_map.insert(table_type='excel',table_name='custom_order',field_name=u'收货县',field_id='county',field_order=9)
    db.db_map.insert(table_type='excel',table_name='custom_order',field_name=u'收货地址',field_id='address',field_order=10)
    db.db_map.insert(table_type='excel',table_name='custom_order',field_name=u'产品编号',field_id='product_id',field_order=11)
    db.db_map.insert(table_type='excel',table_name='custom_order',field_name=u'条形码',field_id='barcode',field_order=12)
    db.db_map.insert(table_type='excel',table_name='custom_order',field_name=u'规格',field_id='specification',field_order=13)
    db.db_map.insert(table_type='excel',table_name='custom_order',field_name=u'网店品名',field_id='ex_product_name',field_order=14)
    db.db_map.insert(table_type='excel',table_name='custom_order',field_name=u'产品名称',field_id='product_name',field_order=15)
    db.db_map.insert(table_type='excel',table_name='custom_order',field_name=u'订货数量',field_id='order_num',field_order=16)
    db.db_map.insert(table_type='excel',table_name='custom_order',field_name=u'网店规格',field_id='ex_spec',field_order=17)

def import_csv(csvfile):
    db.custom_order.import_from_csv_file(csvfile)

def get_feature(s):
    return [s[i:i+2] for i in range(max(len(s)-2+1,1))]
'''
#s=Simhash(get_feature(ws.cell(row=rows,column=10).value,3))
history_data=db().select(db.history_order.order_id,db.history_order.address).as_list()
addr_obj=[(str(k),Simhash(get_feature(v,3))) for k, v in history_data]
index = SimhashIndex(addr_obj, k=3)
or index.get_near_dups(s) is not None
and\(db.history_order.county==ws.cell(row=rows, column=9).value)
rowcontent['relate_history_id']=buf_list[i]['order_id']
rowcontent['wrong_reason']=u'与历史地址第'+str(buf_list[i]['order_id'])+u'地址重复'
if rowcontent['mobile'] in db().select(db.history_order.mobile) :
            rowcontent['wrong_reason']=u'与历史重复'
            db.incorrect_data.insert(**rowcontent)
        else:
            rowcontent['product_tag']=SKU_dict[ws.cell(row=rows,column=12).value]
                s=s.lower()
    s=re.sub(r'[^\w]+','',s)
    db.custom_order.insert(**rowcontent)回族|壮族|维尔吾族|特别行政区|自治区
    &\(re.match('\d{0,2}',db.history_order.product_name).group()==\
                         str(ws1.cell(row=rows,column=10).value))

        if not tablename=='custom_order': raise HTTP(400)
        return dict(custom_order = db.custom_order(id))

'''

def wrong_data():
    response.title = 'wrong_data'
    response.view = 'plugin_sqleditable/sample.html'
    editable = SQLEDITABLE(db.wrong_order, showid=False, maxrow=29).process()
    return dict(editable=editable)

#@auth.requires_login()
def display_form():
    grid = SQLFORM.grid(db.wrong_order,fields=\
        [db.wrong_order.order_id,db.wrong_order.ex_id,db.wrong_order.mobile,
        db.wrong_order.user_name,db.wrong_order.province,db.wrong_order.city,
        db.wrong_order.address,db.wrong_order.wrong_reason,db.wrong_order.dup_ID,
        db.wrong_order.dup_ex,db.wrong_order.dup_address,db.wrong_order.dup_name,
        db.wrong_order.dup_phone])
    return locals()

def display_pampers_result():
    grid = SQLFORM.grid(db.pampers_result)
    return locals()

def display_pampers_order():
    grid = SQLFORM.grid(db.pampers_order)
    return locals()

'''
def data_wrong():
    form = SQLFORM(db.wrong_order)
    if form.process().accepted:
        response.flash = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill out the form'
    return dict(form=form)
'''
def import_excel(file):
    WB=openpyxl.load_workbook(file)
    WS=WB.active
    return WS

def add_excel(ws):
    field_list = db(db.db_map.table_name=='custom_order').select(db.db_map.field_name,db.db_map.field_id).as_list()
    field_dict = {}
    for fd in field_list:
        field_dict[fd['field_name'].decode("utf8")]=fd['field_id']
    header=[] #表头
    for cols in range(1,ws.min_col+1):
        header.append(field_dict[ws.cell(row=1,column=cols).value])
    buf_list=[]
    for rows in range(467,ws.max_row+1):
        rowcontent={}
        for cols in range(1,ws.min_col+1):
            rowcontent[header[cols-1]]=ws.cell(row=rows, column=cols).value
        rowcontent['address']=rowcontent['address'].replace(rowcontent['province']+u'','')
        rowcontent['address']=rowcontent['address'].replace(u''+rowcontent['city'],'')
        rowcontent['address']=rowcontent['address'].replace(rowcontent['county']+u'','')
        if ws.cell(row=rows, column=9).value !=ws.cell(row=rows-1,column=9).value:
            buf_list=db((db.history_order.province==ws.cell(row=rows, column=7).value)&\
                        (db.history_order.city==ws.cell(row=rows, column=8).value)&\
                        (db.history_order.county==ws.cell(row=rows, column=9).value)&\
                        (db.history_order.product_name==SKU_dict[ws.cell(row=rows,column=12).value])).select\
                (db.history_order.mobile,db.history_order.address_bak,db.history_order.order_id,\
                 db.history_order.ex_id,db.history_order.user_name).as_list()
        is_correct=1
        for i in range(0,len(buf_list)):
            if rowcontent['mobile']==buf_list[i]['mobile']:
                is_correct=0
                rowcontent['wrong_reason']=u'与历史号码第'+str(buf_list[i]['order_id'])+u'条重复'
                rowcontent['dup_ID']=buf_list[i]['order_id']
                rowcontent['dup_ex']=buf_list[i]['ex_id']
                rowcontent['dup_address']=buf_list[i]['address_bak']
                rowcontent['dup_name']=buf_list[i]['user_name']
                rowcontent['dup_phone']=buf_list[i]['mobile']
                db.wrong_order.insert(**rowcontent)
                break
            elif Simhash(get_feature(buf_list[i]['address_bak'].decode('UTF-8'))).distance(Simhash(get_feature(u''+rowcontent['address'])))<18:
                is_correct=0
                rowcontent['wrong_reason']=u'与历史地址第'+str(buf_list[i]['order_id'])+u'条重复'
                rowcontent['dup_ID']=buf_list[i]['order_id']
                rowcontent['dup_ex']=buf_list[i]['ex_id']
                rowcontent['dup_address']=buf_list[i]['address_bak']
                rowcontent['dup_name']=buf_list[i]['user_name']
                rowcontent['dup_phone']=buf_list[i]['mobile']
                db.wrong_order.insert(**rowcontent)
                break
            else:continue
        if is_correct==1:
            if rowcontent['user_name']!= ws.cell(row=rows-1, column=6).value:
                rowcontent['product_tag']=SKU_dict[ws.cell(row=rows,column=12).value]
                db.custom_order.insert(**rowcontent)
    for rows in range(2,467):
        rowcontent={}
        for cols in range(1,6+1)+range(11,ws.min_col+1):
            rowcontent[header[cols-1]]=ws.cell(row=rows, column=cols).value
        for prov in provinces:
            if prov in str(ws.cell(row=rows,column=10).value):
                spare_addr=ws.cell(row=rows,column=10).value.replace(prov,'')
                spare_addr=spare_addr.replace(u'省','')
                spare_addr=spare_addr.replace(u'市','')
                if prov in zhixia:
                    rowcontent[header[6]]=prov+u'市'
                elif prov in texing:
                    rowcontent[header[6]]=prov+u'特别行政区'
                elif prov==u'广西':
                    rowcontent[header[6]]=prov+u'壮族自治区'
                elif prov==u'新疆':
                    rowcontent[header[6]]=prov+u'维吾尔自治区'
                elif prov==u'宁夏':
                    rowcontent[header[6]]=prov+u'回族自治区'
                elif prov==u'西藏':
                    rowcontent[header[6]]=prov+u'自治区'
                elif prov==u'内蒙古':
                    rowcontent[header[6]]=prov+u'自治区'
                else:
                    rowcontent[header[6]]=prov+u'省'
                break
            else:
                spare_addr=ws.cell(row=rows,column=10).value
        addr2=re.split(u'市|自治州',spare_addr)
        rowcontent[header[7]]=addr2[0]
        spare_addr2=re.sub(addr2[0],'',spare_addr)
        spare_addr2=re.sub(u'市|自治州','',spare_addr2)

        addr3=re.split(u'县|区',spare_addr2)
        rowcontent[header[8]]=addr3[0]+u'(县)'
        spare_addr3=re.sub(addr3[0],'',spare_addr2)
        spare_addr3=re.sub(u'县|区','',spare_addr3)
        rowcontent[header[9]]=spare_addr3
        if (header[6] not in rowcontent):
            db.address_lack.insert(**rowcontent)
        else:
            buf_list=db((rowcontent[header[6]]==db.history_order.province)&\
                        (db.history_order.product_name==SKU_dict[ws.cell(row=rows,column=12).value])).select\
                (db.history_order.mobile,db.history_order.address,db.history_order.order_id,\
                 db.history_order.ex_id,db.history_order.user_name).as_list()
            is_correct=1
            for i in range(0,len(buf_list)):
                if rowcontent['mobile']==buf_list[i]['mobile']:
                    is_correct=0
                    rowcontent['wrong_reason']=u'与历史号码第'+str(buf_list[i]['order_id'])+u'条重复'
                    rowcontent['dup_ID']=buf_list[i]['order_id']
                    rowcontent['dup_ex']=buf_list[i]['ex_id']
                    rowcontent['dup_address']=buf_list[i]['address']
                    rowcontent['dup_name']=buf_list[i]['user_name']
                    rowcontent['dup_phone']=buf_list[i]['mobile']
                    db.wrong_order.insert(**rowcontent)
                    break
                elif Simhash(get_feature(buf_list[i]['address'])).distance(Simhash(get_feature(ws.cell(row=rows,column=10).value)))<24:
                    is_correct=0
                    rowcontent['wrong_reason']=u'与历史地址第'+str(buf_list[i]['order_id'])+u'条重复'
                    rowcontent['dup_ID']=buf_list[i]['order_id']
                    rowcontent['dup_ex']=buf_list[i]['ex_id']
                    rowcontent['dup_address']=buf_list[i]['address']
                    rowcontent['dup_name']=buf_list[i]['user_name']
                    rowcontent['dup_phone']=buf_list[i]['mobile']
                    db.wrong_order.insert(**rowcontent)
                    break
                else:continue
            if is_correct==1:
                if rowcontent['user_name']!= ws.cell(row=rows-1, column=6).value:
                    rowcontent['product_tag']=SKU_dict[ws.cell(row=rows,column=12).value]
                    db.custom_order.insert(**rowcontent)

pampers_dict={'order_id':'A','ex_id':'B','user_name':'C','mobile':'D','province':'E',
              'city':'F','county':'G','address':'H','pregnancy':'I','product_piece':'J',
              'product_size':'K','datetime':'L'}
def add_pampers(ws1):
    header=['order_id','ex_id','user_name','mobile','province','city','county','address',
            'pregnancy','product_piece','product_size','date_time']
    for rows in range(650,ws1.max_row+1):
        rowcontent={}
        buf_list=[]
        for cols in range(1,ws1.min_col+1):
            rowcontent[header[cols-1]]=u''+str(ws1.cell(row=rows,column=cols).value)
        rowcontent['address']=rowcontent['address'].replace(rowcontent['province'],'')
        rowcontent['address']=rowcontent['address'].replace(rowcontent['city'],'')
        rowcontent['address']=rowcontent['address'].replace(rowcontent['county'],'')
        if ws1.cell(row=rows,column=7).value==ws1.cell(row=rows-1,column=7).value:
            db.pampers_self_dup(**rowcontent)
        elif not isinstance(rowcontent['address'],str):
            db.pampers_addr_lack.insert(**rowcontent)
        else:
            buf_list=db((db.history_order.province==ws1.cell(row=rows, column=5).value)&\
                        (db.history_order.city==ws1.cell(row=rows, column=6).value)&\
                        (db.history_order.county==ws1.cell(row=rows, column=7).value)).select\
                (db.history_order.mobile,db.history_order.address_bak,db.history_order.order_id,
                 db.history_order.ex_id,db.history_order.user_name,db.history_order.product_name).as_list()
        is_correct=1
        for i in range(0,len(buf_list)):
            if (buf_list[i]['product_name'].decode('utf8')).startswith(str(rowcontent['product_piece'])):
                if rowcontent['mobile']==buf_list[i]['mobile']:
                    is_correct=0
                    rowcontent['wrong_reason']=u'与历史号码第'+str(buf_list[i]['order_id'])+u'条重复'
                    rowcontent['dup_ID']=buf_list[i]['order_id']
                    rowcontent['dup_ex']=buf_list[i]['ex_id']
                    rowcontent['dup_address']=buf_list[i]['address_bak']
                    rowcontent['dup_name']=buf_list[i]['user_name']
                    rowcontent['dup_phone']=buf_list[i]['mobile']
                    db.pampers_history_dup.insert(**rowcontent)
                    break
                elif Simhash(get_feature(str(buf_list[i]['address_bak']).decode('UTF-8')))\
                        .distance(Simhash(get_feature(u''+rowcontent['address'])))<5:
                    is_correct=0
                    rowcontent['wrong_reason']=u'与历史地址第'+str(buf_list[i]['order_id'])+u'条重复'
                    rowcontent['dup_ID']=buf_list[i]['order_id']
                    rowcontent['dup_ex']=buf_list[i]['ex_id']
                    rowcontent['dup_address']=buf_list[i]['address_bak']
                    rowcontent['dup_name']=buf_list[i]['user_name']
                    rowcontent['dup_phone']=buf_list[i]['mobile']
                    db.pampers_history_dup.insert(**rowcontent)
                    break
                else:continue
        if is_correct==1:
            if rowcontent['user_name'] ==ws1.cell(row=rows-1,column=3).value:
                db.pampers_self_dup.insert(**rowcontent)
            else:
                if (rowcontent['county'].endswith(u'县'))or\
                (rowcontent['county']==u'清新区')or\
                (rowcontent['county']==u'伊宁市')or\
                (rowcontent['county']==u'万山区')or\
                (rowcontent['county']==u'六枝特区'):
                    if((u'村'in rowcontent['address'])and(u'乡村'not in rowcontent['address']))or\
                    ((u'乡'in rowcontent['address'])and(u'乡村'not in rowcontent['address']))or\
                    ((u'镇'in rowcontent['address'])and(u'小镇'not in rowcontent['address'])):
                        rowcontent['class_city']='village'
                    else:
                        rowcontent['class_city']='D'
                elif (rowcontent['county'].endswith(u'市'))and\
                    (rowcontent['county']!=u'巢湖市')and\
                    (rowcontent['county']!=u'毕节市'):
                    rowcontent['class_city']='C'
                elif (rowcontent['city'] in top4_city):
                    rowcontent['class_city']='Top4'
                elif(rowcontent['city'] in A_city):
                    rowcontent['class_city']='A'
                else:
                    rowcontent['class_city']='B'
                db.pampers_order.insert(**rowcontent)
    for rows in range(1,647):
        rowcontent={}
        for cols in range(1,ws1.min_col+1):
            rowcontent[header[cols-1]]=ws1.cell(row=rows,column=cols).value
        is_addr_complete=1
        flag=0
        for prov in provinces:
            if prov in unicode(ws1.cell(row=rows,column=8).value):
                flag=1
                spare_addr0=ws1.cell(row=rows,column=8).value.replace(prov,'')
                spare_addr0=spare_addr0.replace(u'省','')
                if prov in zhixia:
                    rowcontent[header[4]]=prov
                    rowcontent[header[5]]=prov+u'市'
                    spare_addr1=spare_addr0[spare_addr0.find(u'市')+1:]
                elif prov in texing:
                    rowcontent[header[4]]=prov+u'特别行政区'
                elif prov==u'广西':
                    rowcontent[header[4]]=prov+u'壮族自治区'
                    spare_addr1=spare_addr0.replace(u'壮族自治区','')
                elif prov==u'新疆':
                    rowcontent[header[4]]=prov+u'维吾尔自治区'
                    spare_addr1=spare_addr0.replace(u'维吾尔自治区','')
                elif prov==u'宁夏':
                    rowcontent[header[4]]=prov+u'回族自治区'
                    spare_addr1=spare_addr0.replace(u'回族自治区','')
                elif prov==u'西藏':
                    rowcontent[header[4]]=prov+u'自治区'
                    spare_addr1=spare_addr0.replace(u'自治区','')
                elif prov==u'内蒙古':
                    rowcontent[header[4]]=prov+u'自治区'
                    spare_addr1=spare_addr0.replace(u'自治区','')
                else:
                    rowcontent[header[4]]=prov+u'省'
                    spare_addr1=spare_addr0[spare_addr0.find(u'省')+1:]
                break
        if flag==0:
            is_addr_complete=0
            spare_addr1=ws1.cell(row=rows,column=8).value
        if (u'市'in spare_addr1):
            addr2=spare_addr1[0:spare_addr1.find(u'市')+1]
            spare_addr2=spare_addr1[spare_addr1.find(u'市')+1:]
            rowcontent[header[5]]=addr2
        elif u'自治州'in spare_addr1:
            addr2=spare_addr1[0:spare_addr1.find(u'自治州')+3]
            spare_addr2=spare_addr1[spare_addr1.find(u'自治州')+3:]
            rowcontent[header[5]]=addr2
        elif u'地区'in spare_addr1:
            addr2=spare_addr1[0:spare_addr1.find(u'地区')+2]
            spare_addr2=spare_addr1[spare_addr1.find(u'地区')+2:]
            rowcontent[header[5]]=addr2
        elif u'盟'in spare_addr1:
            addr2=spare_addr1[0:spare_addr1.find(u'盟')+1]
            spare_addr2=spare_addr1[spare_addr1.find(u'盟')+1:]
            rowcontent[header[5]]=addr2
        else:
            spare_addr2=spare_addr1
            if rowcontent[header[4]] not in zhixia:
                is_addr_complete=0

        if u'县'in spare_addr2:
            addr3=spare_addr2[0:spare_addr2.find(u'县')+1]
            spare_addr3=spare_addr2[spare_addr2.find(u'县')+1:]
            rowcontent[header[6]]=addr3
        elif (u'市'in spare_addr2)and (u'超市' not in spare_addr2)and (u'市场' not in spare_addr2):
            addr3=spare_addr2[0:spare_addr2.find(u'市')+1]
            spare_addr3=spare_addr2[spare_addr2.find(u'市')+1:]
            rowcontent[header[6]]=addr3
        elif (u'区'in spare_addr2):
            addr3=spare_addr2[0:spare_addr2.find(u'区')+1]
            spare_addr3=spare_addr2[spare_addr2.find(u'区')+1:]
            rowcontent[header[6]]=addr3
        else:
            spare_addr3=spare_addr2
            is_addr_complete=0

        if is_addr_complete==0:
            db.pampers_addr_lack.insert(**rowcontent)
        else:
            buf_list=db((db.history_order.province==ws1.cell(row=rows, column=5).value)&\
                        (db.history_order.city==ws1.cell(row=rows, column=6).value)&\
                        (db.history_order.county==ws1.cell(row=rows, column=7).value)).select\
                (db.history_order.mobile,db.history_order.address_bak,db.history_order.order_id,
                 db.history_order.ex_id,db.history_order.user_name).as_list()
            is_dup=0
            for i in range(0,len(buf_list)):
                if rowcontent['mobile']==buf_list[i]['mobile']:
                    is_dup=1
                    rowcontent['wrong_reason']=u'与历史号码第'+str(buf_list[i]['order_id'])+u'条重复'
                    rowcontent['dup_ID']=buf_list[i]['order_id']
                    rowcontent['dup_ex']=buf_list[i]['ex_id']
                    rowcontent['dup_address']=buf_list[i]['address']
                    rowcontent['dup_name']=buf_list[i]['user_name']
                    rowcontent['dup_phone']=buf_list[i]['mobile']
                    db.pampers_history_dup.insert(**rowcontent)
                    break
                elif Simhash(get_feature(buf_list[i]['address'])).distance(Simhash(get_feature(ws1.cell(row=rows,column=10).value)))<24:
                    is_dup=1
                    rowcontent['wrong_reason']=u'与历史地址第'+str(buf_list[i]['order_id'])+u'条重复'
                    rowcontent['dup_ID']=buf_list[i]['order_id']
                    rowcontent['dup_ex']=buf_list[i]['ex_id']
                    rowcontent['dup_address']=buf_list[i]['address']
                    rowcontent['dup_name']=buf_list[i]['user_name']
                    rowcontent['dup_phone']=buf_list[i]['mobile']
                    db.pampers_history_dup.insert(**rowcontent)
                    break
                else:continue
            if is_dup==0:
                if rowcontent['user_name']== ws1.cell(row=rows-1, column=3).value:
                    db.pampers_self_dup(**rowcontent)
                else:
                    if (rowcontent['county'].endswith(u'县'))or\
                    (rowcontent['county']==u'清新区')or\
                    (rowcontent['county']==u'伊宁市')or\
                    (rowcontent['county']==u'万山区')or\
                    (rowcontent['county']==u'六枝特区'):
                        if((u'村'in rowcontent['address'])and(u'乡村'not in rowcontent['address']))or\
                        ((u'乡'in rowcontent['address'])and(u'乡村'not in rowcontent['address']))or\
                        ((u'镇'in rowcontent['address'])and(u'小镇'not in rowcontent['address'])):
                            rowcontent['class_city']='village'
                        else:
                            rowcontent['class_city']='D'
                    elif (rowcontent['county'].endswith(u'市'))and\
                        (rowcontent['county']!=u'巢湖市')and\
                        (rowcontent['county']!=u'毕节市'):
                        rowcontent['class_city']='C'
                    elif (rowcontent['city'] in top4_city):
                        rowcontent['class_city']='Top4'
                    elif(rowcontent['city'] in A_city):
                        rowcontent['class_city']='A'
                    else:
                        rowcontent['class_city']='B'
                    db.pampers_order.insert(**rowcontent)

def pampers_census():
    row_content={}
    row_content['tag']='November'
    row_content['distribution']=db(db.pampers_order.order_id >= 0).count()
    row_content['Top4']=db(db.pampers_order.class_city=='Top4').count()
    row_content['A_city']=db(db.pampers_order.class_city=='A').count()
    row_content['B_city']=db(db.pampers_order.class_city=='B').count()
    row_content['C_city']=db(db.pampers_order.class_city=='C').count()
    row_content['D_city']=db(db.pampers_order.class_city=='D').count()
    row_content['village']=db(db.pampers_order.class_city=='village').count()
    db.pampers_result.insert(**row_content)
    row_content={}
    row_content['tag']='percent'
    row_content['distribution']='100%'
    row_content['Top4']=float(db(db.pampers_order.class_city=='Top4').count())/db(db.pampers_order.order_id >= 0).count()
    row_content['A_city']=float(db(db.pampers_order.class_city=='A').count())/db(db.pampers_order.order_id >= 0).count()
    row_content['B_city']=float(db(db.pampers_order.class_city=='B').count())/db(db.pampers_order.order_id >= 0).count()
    row_content['C_city']=float(db(db.pampers_order.class_city=='C').count())/db(db.pampers_order.order_id >= 0).count()
    row_content['D_city']=float(db(db.pampers_order.class_city=='D').count())/db(db.pampers_order.order_id >= 0).count()
    row_content['village']=float(db(db.pampers_order.class_city=='village').count())/db(db.pampers_order.order_id >= 0).count()
    db.pampers_result.insert(**row_content)

def add_PG(ws3):
    product_dict={}
    header=['SB_Internal_Member_ID','Member_Account_ID','Reward_ID','Reward_Name','Reward_Value',
        'Reward_Points','Reward_Internal_Cost','Issue_Date','Issue_Location','Redeemed_Date',
        'Redeemed_Location','Cancel_Date','Expiration_Date','Reward_Barcode','First_Name','Last_Name',
        'Address','City','trade_state','ZipCode','Email_Address','Mobil_Phone','IssuedFlag','RedeemFlag',
        'CanceledFlag','REDEMPTION_STATUS','DLVRYNBR_REJRSN','DELIVERY_ADDRESS']
    for rows in range(1,ws3.max_row+1):
        rowcontent={}
        buf_list=[]
        for cols in range(1,ws3.min_col+1):
            rowcontent[header[cols-1]]=unicode(ws3.cell(row=rows,column=cols).value)
        db.original_data.insert(**rowcontent)
#product id detribute info
    rows= db().select(db.original_data.Reward_Name,
                db.original_data.Reward_Value,
                db.original_data.Reward_Points,
                db.original_data.Reward_Internal_Cost,
                orderby=db.original_data.Reward_Name)
    rows[0]['product_id']=1*100+37
    product_id=1*100+37
    product_dict[rows[0]['Reward_Name']]=rows[0]['product_id']
    db.product_info.insert(**rows[0])
    for i in range(1,len(rows)):
        if (rows[i]['Reward_Name']!=rows[i-1]['Reward_Name'])or\
        (rows[i]['Reward_Value']!=rows[i-1]['Reward_Value'])or\
        (rows[i]['Reward_Points']!=rows[i-1]['Reward_Points'])or\
        (rows[i]['Reward_Internal_Cost']!=rows[i-1]['Reward_Internal_Cost']):
            rows[i]['product_id']=product_id+100
            product_id=rows[i]['product_id']
            product_dict[rows[i]['Reward_Name']]=rows[i]['product_id']
            db.product_info.insert(**rows[i])
        else:pass
#user id detribute info
    user_row={}
    users_address=[]
    address_buf={}
    users= db(db.original_data.DELIVERY_ADDRESS !=None).select\
            (db.original_data.SB_Internal_Member_ID,
             db.original_data.Member_Account_ID,
             db.original_data.DELIVERY_ADDRESS,
             db.original_data.Reward_Name,
             orderby=db.original_data.DELIVERY_ADDRESS)
    users_address=((users[0]['DELIVERY_ADDRESS']).decode('utf8')).split(";")
    user_row['user_name']=users_address[0]
    address_buf['user_name']=users_address[0]
    user_row['address']=users_address[1]
    address_buf['address']=users_address[1]
    user_row['phone_num']=users_address[2]
    address_buf['phone_num']=users_address[2]
    user_row['city']=users_address[3]
    user_row['province']=users_address[4]
    user_row['zip_code']=users_address[5]
    user_row['Country']=users_address[6]
    user_row['SB_Internal_Member_ID']=unicode(users[0]['SB_Internal_Member_ID'])
    user_row['Member_Account_ID']=unicode(users[0]['Member_Account_ID'])
    user_row['user_id']=1*100+79
    user_id=1*100+79
    db.user_info.insert(**user_row)

    for i in range(1,len(users)):
        users_address=((users[i]['DELIVERY_ADDRESS']).decode('utf8')).split(";")
        if len(users_address)==7:
            user_row['user_name']=users_address[0]
            user_row['address']=users_address[1]
            user_row['phone_num']=users_address[2]
            user_row['city']=users_address[3]
            user_row['province']=users_address[4]
            user_row['zip_code']=users_address[5]
            user_row['Country']=users_address[6]
            user_row['SB_Internal_Member_ID']=unicode(users[0]['SB_Internal_Member_ID'])
            user_row['Member_Account_ID']=unicode(users[0]['Member_Account_ID'])
            w1=(user_row['phone_num']==address_buf['phone_num'])
            w2=(Simhash(get_feature(user_row['address'])).distance(Simhash(get_feature(address_buf['address'])))<5)
            w3=(user_row['user_name']==address_buf['user_name'])
            if (w1*0.5+w2*0.3+w3*0.2)<0.5:
                user_row['user_id']=user_id+100
                user_id=user_row['user_id']
                db.user_info.insert(**user_row)
                address_buf['phone_num']=user_row['phone_num']
                address_buf['address']=user_row['address']
                address_buf['user_name']=user_row['user_name']
            else:pass
#user2product
    all_user=db().select(db.user_info.ALL)
    for each in range(0,len(all_user)):
        u2p_row={}
        u2p_row['product_id']=[]
        u2p_row['trials_count']=[]
        u2p_row['user_id']=all_user[each]['user_id']
        u2p_ship=db(int(all_user[each]['Member_Account_ID'])==db.original_data.Member_Account_ID).select\
                (db.original_data.Reward_Name)
        all_product=[]
        all_product.append(u2p_ship[0]['Reward_Name'])
        if len(u2p_ship)>=2:
            for j in range(1,len(u2p_ship)):
                if u2p_ship[j]['Reward_Name'] != u2p_ship[j-1]['Reward_Name']:
                    all_product.append(u2p_ship[j]['Reward_Name'])
        for k in range(0,len(all_product)):
            (u2p_row['product_id']).append(all_product[k])
            each_product_count=all_product.count(all_product[k])
            (u2p_row['trials_count']).append(int(each_product_count))
        db.user2product.insert(**u2p_row)
        del all_product
        del u2p_ship
        u2p_row.clear()
def display_u2p():
    grid = SQLFORM.grid(db.user2product)
    return locals()


def add_babybox_BBS_CD(ws4):
    header_babybox=['order_id','trade_order','trade_id','ex_id','product_order','barcode',
                    'username','cellphone','province','city','county','address','reserve1',
                    'product_name','data_date','channel','moon','reserve2','product','product_size',
                    'product_brand','store_size','product_quantity','store_name',
                    'receive_province','receive_city','receive_county','receive_address']
    header_BBS=[]
    header_FSCD=[]
    SameOneHouse_phonenum=[]
    town5times_phonenum=[]
    village3times_phonenum=[]
    AddressBlur_phonenum=[]
    cor=[]
    incor=[]
    field_list = header_babybox
    table_header={}
    for cols in range(1,ws4.min_col+1):
        table_header[field_list[cols-1]]=ws4.cell(row=1,column=cols).value
    for rows in range(2,ws4.max_row+1):
        rowcontent={}
        for cols in range(1,ws4.min_col+1):
            rowcontent[field_list[cols-1]]=ws4.cell(row=rows,column=cols).value
        address=rowcontent['address']
        if address.endswith(u'市')or address.endswith(u'县')or\
        address.endswith(u'镇')or address.endswith(u'工业区')or address.endswith(u'工业园区')or\
        address.endswith(u'公园')or address.endswith(u'管理区')or address.endswith(u'开发区')or\
        address.endswith(u'新区')or address.endswith(u'球场')or address.endswith(u'停车场')or\
        address.endswith(u'篮球场')or address.endswith(u'大道')or address.endswith(u'国道')or\
        address.endswith(u'道')or address.endswith(u'路')or address.endswith(u'桥')or\
        address.endswith(u'路口')or address.endswith(u'街上')or address.endswith(u'街')or\
        address.endswith(u'门口')or address.endswith(u'市场')or address.endswith(u'公交站')or\
        address.endswith(u'车站')or address.endswith(u'加油站')or address.endswith(u'服务站')or\
        address.endswith(u'自取')or address.endswith(u'交叉口')or address.endswith(u'三岔口')or\
        address.endswith(u'桥头')or address.endswith(u'附近')or address.endswith(u'快递')or\
        address.endswith(u'物流')or address.endswith(u'自取')or address.endswith(u'交口'):
            incor.append(rowcontent['cellphone'])
        elif address.endswith(u'号楼') or address.endswith(u'栋')or\
        address.endswith(u'幢') or address.endswith(u'座'):
            SameOneHouse_phonenum.append(rowcontent['cellphone'])
        elif address.endswith(u'小区')or address.endswith(u'校区')or\
        address.endswith(u'宿舍')or address.endswith(u'公寓')or\
        address.endswith(u'期')or address.endswith(u'A区')or\
        address.endswith(u'B区')or address.endswith(u'C区')or\
        address.endswith(u'D区')or address.endswith(u'东区')or\
        address.endswith(u'西区')or address.endswith(u'北区')or\
        address.endswith(u'南区'):
            town5times_phonenum.append(rowcontent['cellphone'])
        elif address.endswith(u'乡')or address.endswith(u'村')or address.endswith(u'庄')or\
        address.endswith(u'营')or address.endswith(u'寨')or address.endswith(u'崖')or\
        address.endswith(u'矿')or address.endswith(u'岗')or address.endswith(u'沟')or\
        address.endswith(u'集')or address.endswith(u'湾')or address.endswith(u'小学')or\
        address.endswith(u'中学')or  address.endswith(u'大学')or address.endswith(u'厂')or\
        address.endswith(u'街道')or address.endswith(u'里')or address.endswith(u'巷')or\
        address.endswith(u'弄')or address.endswith(u'社区')or address.endswith(u'中心')or\
        address.endswith(u'办事处')or address.endswith(u'政府单位')or address.endswith(u'局')or\
        address.endswith(u'法院')or address.endswith(u'医院')or address.endswith(u'大厦')or\
        address.endswith(u'居委会')or address.endswith(u'派出所')or address.endswith(u'汽配城')or\
        address.endswith(u'商贸城')or address.endswith(u'速递易')or address.endswith(u'镇邮局'):
            village3times_phonenum.append(rowcontent['cellphone'])
        elif address.endswith(u'侧') or address.endswith(u'旁')or address.endswith(u'边')or\
        address.endswith(u'隔壁')or address.endswith(u'附近')or address.endswith(u'对面')or \
        address.endswith(u'段'):#or address.endswith(u'门口') or address.endswith(u'口') :
            AddressBlur_phonenum.append(rowcontent['cellphone'])
        else:
            cor.append(rowcontent['cellphone'])

    for rows in range(2,ws4.max_row+1):
        rowcontent={}
        correct_phonenum=SameOneHouse_phonenum + town5times_phonenum + \
                        village3times_phonenum + AddressBlur_phonenum
        phonenum = ws4.cell(row=rows,column=8).value
        for cols in range(1,ws4.min_col+1):
            rowcontent[field_list[cols-1]]=ws4.cell(row=rows,column=cols).value
        if phonenum in incor:
            db.incorrect_BCB.insert(**rowcontent)
        elif phonenum in cor:
            db.correct_BCB.insert(**rowcontent)
        elif phonenum in SameOneHouse_phonenum:
            if SameOneHouse_phonenum.count(phonenum)>=2:
                db.incorrect_BCB.insert(**rowcontent)
            else:
                db.correct_BCB.insert(**rowcontent)
        elif phonenum in town5times_phonenum:
            if (town5times_phonenum.count(phonenum)>5):
                db.incorrect_BCB.insert(**rowcontent)
            else:
                db.correct_BCB.insert(**rowcontent)
        elif phonenum in village3times_phonenum:
            if village3times_phonenum.count(phonenum)>3:
                db.incorrect_BCB.insert(**rowcontent)
            else:
                db.correct_BCB.insert(**rowcontent)
        elif phonenum in AddressBlur_phonenum:
            if AddressBlur_phonenum.count(phonenum)>=2:
                db.incorrect_BCB.insert(**rowcontent)
            else:
                db.correct_BCB.insert(**rowcontent)
        else:pass

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    #response.flash = T("Hello World")
    #return dict(message=T('Welcome to web2py!'))
    if request.vars.csvfile1 != None:
        ws=import_excel(request.vars.csvfile1.file)
        add_excel(ws)
        response.flash = T('data uploaded')
    if request.vars.csvfile3 != None:
        ws3=import_excel(request.vars.csvfile3.file)
        add_PG(ws3)
        response.flash = T('data uploaded')
    if request.vars.csvfile4 != None:
        ws4=import_excel(request.vars.csvfile4.file)
        add_babybox_BBS_CD(ws4)
        response.flash = T('data uploaded')
    if request.vars.csvfile2 != None:
        ws1=import_excel(request.vars.csvfile2.file)
        lice=[1516161,1520345,1518691,1542961,1551748,1541116,1516035,1520803,
        1522679,1527299,1538111,1544564,1550749,1520841,1540979,1523641]
        if db(db.pampers_order).isempty():
            add_pampers(ws1)
            response.flash = T('data uploaded')
        else:
            count=0
            for i in range(0,len(lice)):
                if(ws1.cell(row=i,column=1).value==lice[i]):
                    count=count+1
            if count>11:
                add_pampers(ws1)
                response.flash = T('data uploaded')
            else:pass
        pampers_census()
    return dict()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

#@auth.requires_login()
@request.restful()
def TradeAdd():
    response.view ='generic.'+request.extension  #return  json
    def POST(tablename,**vars):
        ret={}
        #if db(db.trade).isempty():
        ret=dict(db[tablename].validate_and_insert(**vars))
        '''else:
            samp_list=db().select(db.trade.mobilPhone,
            db.trade.postcode,db.trade.consignee,db.trade.address).as_list()
            for i in range(0,len(samp_list)):
                w1=(vars['mobilPhone']==samp_list[i]['mobilPhone'])
                w2=(vars['postcode']==samp_list[i]['postcode'])and \
                   (Simhash(get_feature(vars['address'])).distance(Simhash(get_feature(samp_phonenum[i]['address'])))<5)
                w3=(vars['consignee']==samp_list[i]['consignee'])
                if (w1*0.5+w2*0.3+w3*0.2)>0.5:
                    ret=dict(db[tablename].validate_and_insert(**vars))
                else:
                    ret["errors"]={"WrongReason":"duplication"}'''
        return ret
            #else:raise HTTP(400)
    return locals()

@auth.requires_login()
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


