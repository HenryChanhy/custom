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

provinces=(u'北京',u'天津',u'河北',u'山西',u'内蒙古',u'辽宁',u'吉林',u'黑龙江',u'上海',u'江苏',
           u'浙江',u'安徽',u'福建',u'江西',u'山东',u'河南',u'湖北',u'湖南',u'广东',u'广西',
           u'海南',u'重庆',u'四川',u'贵州',u'云南',u'西藏',u'陕西',u'甘肃',u'青海',u'宁夏',
           u'新疆',u'香港',u'澳门',u'台湾')
zhixia=(u'北京',u'天津',u'重庆',u'上海')
texing=(u'香港',u'澳门')
SKU_dict={u'589203710279202':u'(18片装)S',
u'690314820783301':u'(18片装)NB',
u'589203710279204':u'(8片装)S',
u'690314820785503':u'(8片装)NB'}

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

def get_feature(s,width):
    s=s.lower()
    s=re.sub(r'[^\w]+','',s)
    return [s[i:i+width] for i in range(max(len(s)-width+1,1))]
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
            db.custom_order.insert(**rowcontent)回族|壮族|维尔吾族|特别行政区|自治区'''


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
        buf_list=db(rowcontent[header[6]]==db.history_order.province).select\
                (db.history_order.mobile,db.history_order.address,db.history_order.order_id).as_list()
        is_correct=1
        for i in range(0,len(buf_list)):
            if rowcontent['mobile']==buf_list[i]['mobile']:
                is_correct=0
                rowcontent['wrong_reason']=u'与历史号码第'+str(buf_list[i]['order_id'])+u'条重复'
                rowcontent['dup_ID']=buf_list[i]['order_id']
                db.wrong_order.insert(**rowcontent)
                break
            elif Simhash(get_feature(buf_list[i]['address'],3)).distance(Simhash(get_feature(ws.cell(row=rows,column=10).value,3)))<6:
                is_correct=0
                rowcontent['wrong_reason']=u'与历史地址第'+str(buf_list[i]['order_id'])+u'条重复'
                rowcontent['dup_ID']=buf_list[i]['order_id']
                db.wrong_order.insert(**rowcontent)
                break
            else:break
        if is_correct==1:
            rowcontent['product_tag']=SKU_dict[ws.cell(row=rows,column=12).value]
            if rowcontent['user_name']!= ws.cell(row=rows-1, column=6).value:
                db.custom_order.insert(**rowcontent)
    buf_list=[]
    for rows in range(467,ws.max_row+1):
        rowcontent={}
        for cols in range(1,ws.min_col+1):
            rowcontent[header[cols-1]]=ws.cell(row=rows, column=cols).value
        if ws.cell(row=rows, column=9).value !=ws.cell(row=rows-1,column=9):
            buf_list=db((db.history_order.province==ws.cell(row=rows, column=7).value)&\
                        (db.history_order.city==ws.cell(row=rows, column=8).value)&\
                        (db.history_order.county==ws.cell(row=rows, column=9).value)).select\
                (db.history_order.mobile,db.history_order.address_bak,db.history_order.order_id).as_list()
        is_correct=1
        for i in range(0,len(buf_list)):
            if rowcontent['mobile']==buf_list[i]['mobile']:
                is_correct=0
                rowcontent['wrong_reason']=u'与历史号码第'+str(buf_list[i]['order_id'])+u'条重复'
                rowcontent['dup_ID']=buf_list[i]['order_id']
                db.wrong_order.insert(**rowcontent)
                break
            elif Simhash(get_feature(buf_list[i]['address_bak'],3)).distance(Simhash(get_feature(rowcontent['address'],3)))<5:
                is_correct=0
                rowcontent['wrong_reason']=u'与历史地址第'+str(buf_list[i]['order_id'])+u'条重复'
                rowcontent['dup_ID']=buf_list[i]['order_id']
                db.wrong_order.insert(**rowcontent)
                break
            else:break
        if is_correct==1:
            rowcontent['product_tag']=SKU_dict[ws.cell(row=rows,column=12).value]
            if rowcontent['user_name']!= ws.cell(row=rows-1, column=6).value:
                db.custom_order.insert(**rowcontent)

'''
def db_test():
    row_content={}
    row_content['order_id']=u'S1508280000159'
    row_content['ex_id']=u'PP01592111'
    row_content['telephone']=13433932028
    row_content['mobile']=13433932028
    row_content['user_name']=u'唐惠敏'
    row_content['province']=u'广东'
    row_content['city']=u'广州'
    row_content['county']=u'萝岗'
    row_content['address']=u'广东省广州市萝岗区笔岗斗园新村环街4号501房'
    row_content['product_id']=2015012202
    row_content['barcode']=690314820785503
    row_content['specification']=u'统一规格'
    row_content['ex_product_name']=u'帮宝适特级棉柔'
    row_content['product_name']=u'NB号8片装'
    row_content['order_num']=1
    row_content['ex_spec']=u'nb'
    row_content['wrong_reason']=u'与历史18片重复'
    db.incorrect_dada.insert(**row_content)
'''

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
#    response.flash = T("Hello World")
#    return dict(message=T('Welcome to web2py!'))
    if request.vars.csvfile != None:
        import_excel(request.vars.csvfile.file)
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
