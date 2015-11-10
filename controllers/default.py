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
import openpyxl
from plugin_sqleditable.editable import SQLEDITABLE
SQLEDITABLE.init()

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
'''

def wrong_data():
    response.title = 'wrong_data'
    response.view = 'plugin_sqleditable/sample.html'
    editable = SQLEDITABLE(db.wrong_order, showid=False, maxrow=29).process()
    return dict(editable=editable)

#@auth.requires_login()
def display_form():
    grid = SQLFORM.grid(db.wrong_order,fields=\
        [db.wrong_order.order_id,db.wrong_order.ex_id,db.wrong_order.mobile,\
        db.wrong_order.user_name,db.wrong_order.province,db.wrong_order.city,\
        db.wrong_order.address,db.wrong_order.wrong_reason,db.wrong_order.dup_ID,\
        db.wrong_order.dup_ex,db.wrong_order.dup_address,db.wrong_order.dup_name,\
        db.wrong_order.dup_phone])
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
    wb=openpyxl.load_workbook(file)
    ws=wb.active
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
        if ws.cell(row=rows, column=9).value !=ws.cell(row=rows-1,column=9):
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
                spare_addr=re.sub(prov,'',ws.cell(row=rows,column=10).value)
                spare_addr=re.sub(u'省|^市?' ,'',spare_addr)
                if prov in zhixia:
                    rowcontent[header[6]]=prov+u'市'
                elif prov in texing:
                    rowcontent[header[6]]=prov+u'特别行政区'
                elif prov==u'广西':
                    rowcontent[header[6]]=prov+u'壮族自治区'
                elif prov==u'新疆':
                    rowcontent[header[6]]=prov+u'维尔吾族自治区'
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


pampers_dict={'order_id':'A','ex_id':'B','user_name':'C','mobile':'D','province':'E',\
                  'city':'F','county':'G','address':'H','pregnancy':'I','product_piece':'J',\
                  'product_size':'K','datetime':'L'}
def add_pampers(file):
    wb1=openpyxl.load_workbook(file)
    ws1=wb1.active
    header=['order_id','ex_id','user_name','mobile','province','city','county','address',\
            'pregnancy','product_piece','product_size','date_time']
    for rows in range(650,ws1.max_row+1):
        rowcontent={}
        for cols in range(1,ws1.min_col+1):
            rowcontent[header[cols-1]]=ws1.cell(row=rows,column=cols).value
        rowcontent['address']=re.sub(rowcontent['province'],'',rowcontent['address'])
        rowcontent['address']=re.sub(rowcontent['city'],'',rowcontent['address'])
        rowcontent['address']=re.sub(rowcontent['county'],'',rowcontent['address'])
        if ws1.cell(row=rows,column=7).value !=ws1.cell(row=rows-1,column=7).value:
            buf_list=db((db.history_order.province==ws1.cell(row=rows, column=5).value)&\
                        (db.history_order.city==ws1.cell(row=rows, column=6).value)&\
                        (db.history_order.county==ws1.cell(row=rows, column=7).value)).select\
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
                db.pampers_history_dup.insert(**rowcontent)
                break
            elif Simhash(get_feature(buf_list[i]['address_bak'].decode('UTF-8'))).distance(Simhash(get_feature(u''+rowcontent['address'])))<5:
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
            if rowcontent['user_name']!= ws1.cell(row=rows-1, column=6).value:
                db.pampers_order.insert(**rowcontent)
            else:db.pampers_self_dup.insert(**rowcontent)


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
        import_excel(request.vars.csvfile1.file)
        response.flash = T('data uploaded')
    if request.vars.csvfile2 != None:
        add_pampers(request.vars.csvfile2.file)
        response.flash = T('data uploaded')
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
