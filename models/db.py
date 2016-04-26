# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'], fake_migrate_all=True)
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb',migrate=True)
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*.xml','*.json'] #if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()
## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################
db.define_table('history_order',
                Field('mobilPhone',length=20,unique=True),
                Field('out_tid',length=20),
                Field('province',length=20),
                Field('city',length=20),
                Field('area',length=20),
                Field('address',length=100,notnull=True),
                Field('shop_id',length=20),
                Field('storage_id',length=20),
                Field('consignee',length=20),
                Field('postcode',length=20),
                Field('city_level',length=20),
                Field('product_channel',length=20),
                Field('express',length=20),
                Field('order_type',length=20),
                Field('process_status',length=20),
                Field('pay_status',length=20),
                Field('deliver_status',length=20),
                Field('order_date',type='datetime'),
                Field('data_date',length=20),
                Field('plat_type',length=20),
                Field('barCode',length=20),
                Field('product_title',length=20),
                Field('standard',length=20),
                Field('backupinfo',length=20),
                Field('examine_status',length=20),
                Field('addr_hash')
                )

db.define_table('history',
                Field('order_id', unique=True,length=20),
                Field('ex_id',length=20),
                Field('promo_id',length=20),
                Field('barcode',length=20),
                Field('user_name',length=40),
                Field('mobile',length=13),
                Field('province',length=40),
                Field('city',length=40),
                Field('county',length=40),
                Field('address',length=80),
                Field('order_date',length=13),
                Field('product_name',length=20),
                Field('data_date',length=20),
                Field('channel',length=13),
                Field('stage',length=20),
                Field('city_class1',length=20),
                Field('city_class2',length=20),
                Field('memo1',length=20),
                Field('memo2',length=20),
                Field('address_bak',length=20)
                )
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
db.define_table('db_map',
                Field('table_type',length=20),
                Field('table_name',length=40),
                Field('field_name',length=40),
                Field('field_id',length=40),
                Field('field_order',type='integer'),
                Field('votes','integer',default=0))

db.define_table('custom_order',
                Field('order_id', unique=True,length=20),
                Field('shop_name',length=40),
                Field('ex_id',length=20),
                Field('telephone',length=13),
                Field('mobile',length=13),
                Field('user_name',length=40),
                Field('province',length=40),
                Field('city',length=40),
                Field('county',length=40),
                Field('address',length=80),
                Field('product_id',length=40),
                Field('barcode',length=20),
                Field('specification',length=40),
                Field('ex_product_name',length=40),
                Field('product_name',length=40),
                Field('order_num',type='integer'),
                Field('ex_spec',length=40),
                Field('product_tag',length=40)
                )

#the address is not complete
db.define_table('address_lack',
                Field('order_id', unique=True,length=20),
                Field('shop_name',length=40),
                Field('ex_id',length=20),
                Field('telephone',length=13),
                Field('mobile',length=13),
                Field('user_name',length=40),
                Field('province',length=40),
                Field('city',length=40),
                Field('county',length=40),
                Field('address',length=80),
                Field('product_id',length=40),
                Field('barcode',length=20),
                Field('specification',length=40),
                Field('ex_product_name',length=40),
                Field('product_name',length=40),
                Field('order_num',type='integer'),
                Field('ex_spec',length=40)
                )

db.define_table('wrong_order',
                Field('order_id', unique=True,length=20),
                Field('shop_name',length=40),
                Field('ex_id',length=20),
                Field('telephone',length=13),
                Field('mobile',length=13),
                Field('user_name',length=40),
                Field('province',length=40),
                Field('city',length=40),
                Field('county',length=40),
                Field('address',length=80),
                Field('product_id',length=40),
                Field('barcode',length=20),
                Field('specification',length=40),
                Field('ex_product_name',length=40),
                Field('product_name',length=40),
                Field('order_num',type='integer'),
                Field('ex_spec',length=40),
                Field('wrong_reason',length=40),
                Field('dup_ID',length=40),
                Field('dup_ex',length=80),
                Field('dup_address',length=80),
                Field('dup_name',length=80),
                Field('dup_phone',length=80)
                )

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
db.define_table('pampers_order',
                Field('order_id', unique=True,length=20),
                Field('ex_id',length=20),
                Field('user_name',length=40),
                Field('mobile',length=13),
                Field('province',length=40),
                Field('city',length=40),
                Field('county',length=40),
                Field('address',length=80),
                Field('pregnancy',length=40),
                Field('product_piece',length=40),
                Field('product_size',length=40),
                Field('date_time',length=20),
                Field('class_city',length=20)
                )
db.define_table('pampers_history_dup',
                Field('order_id', unique=True,length=20),
                Field('ex_id',length=20),
                Field('user_name',length=40),
                Field('mobile',length=13),
                Field('province',length=40),
                Field('city',length=40),
                Field('county',length=40),
                Field('address',length=80),
                Field('pregnancy',length=40),
                Field('product_piece',length=40),
                Field('product_size',length=40),
                Field('date_time',length=20),
                Field('wrong_reason',length=40),
                Field('dup_ID',length=40),
                Field('dup_ex',length=80),
                Field('dup_address',length=80),
                Field('dup_name',length=80),
                Field('dup_phone',length=80)
                )
db.define_table('pampers_self_dup',
                Field('order_id', unique=True,length=20),
                Field('ex_id',length=20),
                Field('user_name',length=40),
                Field('mobile',length=13),
                Field('province',length=40),
                Field('city',length=40),
                Field('county',length=40),
                Field('address',length=80),
                Field('pregnancy',length=40),
                Field('product_piece',length=40),
                Field('product_size',length=40),
                Field('date_time',length=20)
                )
db.define_table('pampers_addr_lack',
                Field('order_id', unique=True,length=20),
                Field('ex_id',length=20),
                Field('user_name',length=40),
                Field('mobile',length=13),
                Field('province',length=40),
                Field('city',length=40),
                Field('county',length=40),
                Field('address',length=80),
                Field('pregnancy',length=40),
                Field('product_piece',length=40),
                Field('product_size',length=40),
                Field('date_time',length=20)
                )
db.define_table('pampers_result',
                Field('tag',length=40),
                Field('distribution',length=20),
                Field('Top4',length=20),
                Field('A_city',length=20),
                Field('B_city',length=20),
                Field('C_city',length=20),
                Field('D_city',length=20),
                Field('village',length=20)
                )
###############################################################
db.define_table('trade',
                Field('tid',length=20),
                Field('out_tid',length=20),
                Field('shop_id',length=20),
                Field('storage_id',length=20),
                Field('buyer_id',length=20),
                Field('buyer_msg',length=20),
                Field('buyer_email',length=20),
                Field('buyer_alipay',length=20),
                Field('seller_remark',length=20),
                Field('consignee',length=20),
                Field('address',length=100),
                Field('postcode',length=20),
                Field('telephone',length=20),
                Field('mobilPhone',length=20),
                Field('province',length=20),
                Field('city',length=20),
                Field('city_class',length=10),
                Field('area',length=20),
                Field('actual_freight_get',length=20),
                Field('actual_RP',length=20),
                Field('ship_method',length=20),
                Field('express',length=20),
                Field('is_invoiceOpened',length=20),
                Field('invoice_type',length=20),
                Field('invoice_money',length=20),
                Field('invoice_title',length=20),
                Field('invoice_msg',length=20),
                Field('order_type',length=20),
                Field('process_status',length=20),
                Field('pay_status',length=20),
                Field('deliver_status',length=20),
                Field('is_COD',length=20),
                Field('serverCost_COD',length=20),
                Field('order_totalMoney',length=20),
                Field('product_totalMoney',length=20),
                Field('pay_method',length=20),
                Field('pay_commission',length=20),
                Field('pay_score',length=20),
                Field('return_score',length=20),
                Field('favorable_money',length=20),
                Field('alipay_transaction_no',length=20),
                Field('out_payNo',length=20),
                Field('out_express_method',length=20),
                Field('out_order_status',length=20),
                Field('order_date',type='datetime'),
                Field('pay_date',length=20),
                Field('finish_date',length=20),
                Field('plat_type',length=20),
                Field('distributor_no',length=20),
                Field('WuLiu',length=20),
                Field('WuLiu_no',length=20),
                Field('in_memo',length=20),
                Field('other_remark',length=20),
                Field('actual_freight_pay',length=20),
                Field('ship_date_plan',length=20),
                Field('deliver_date_plan',length=20),
                Field('is_scorePay',length=20),
                Field('is_needInvoice',length=20),
                Field('barCode',length=20),
                Field('product_title',length=20),
                Field('standard',length=20),
                Field('out_price',length=20),
                Field('favorite_money',length=20),
                Field('orderGoods_Num',length=20),
                Field('gift_Num',length=20),
                Field('cost_Price',length=20),
                Field('t_id',length=20),
                Field('product_stockout',length=20),
                Field('is_Book',length=20),
                Field('is_presell',length=20),
                Field('is_Gift',length=20),
                Field('avg_price',length=20),
                Field('product_freight',length=20),
                Field('shop__id',length=20),
                Field('out__tid',length=20),
                Field('out_productId',length=20),
                Field('out_barCode',length=20),
                Field('product_intro',length=20),
                Field('status',length=20),
                Field('tc_return',length=20),
                Field('edb_return'),
                Field('oti_return'),
                Field('sim_trade')
                )
db.define_table('AllBarcode',
                Field('product_num',length=20),
                Field('product_id',length=20),
                Field('product_size',length=20),
                Field('product_name',length=20),
                Field('bar_code',length=20),
                Field('brand',length=20),
                Field('product_classify',length=20),
                )
db.define_table('WuLiuInfo',
                Field('orderId',length=20),
                Field('order_status',length=20),
                Field('logisticCompany',length=20),
                Field('trackingNo',length=20),
                Field('updateTime',type='datetime')
                )
################### P&G ############################################
db.define_table('original_data',
                Field('SB_Internal_Member_ID',length=20),
                Field('Member_Account_ID',length=20),
                Field('Reward_ID',length=20),
                Field('Reward_Name',length=20),
                Field('Reward_Value',length=20),
                Field('Reward_Points',length=20),
                Field('Reward_Internal_Cost',length=20),
                Field('Issue_Date',length=20),
                Field('Issue_Location',length=20),
                Field('Redeemed_Date',length=20),
                Field('Redeemed_Location',length=20),
                Field('Cancel_Date',length=20),
                Field('Expiration_Date',length=20),
                Field('Reward_Barcode',length=20),
                Field('First_Name',length=20),
                Field('Last_Name',length=20),
                Field('Address',length=20),
                Field('City',length=20),
                Field('trade_state',length=20),
                Field('ZipCode',length=20),
                Field('Email_Address',length=20),
                Field('Mobil_Phone',length=20),
                Field('IssuedFlag',length=20),
                Field('RedeemFlag',length=20),
                Field('CanceledFlag',length=20),
                Field('REDEMPTION_STATUS',length=20),
                Field('DLVRYNBR_REJRSN',length=20),
                Field('DELIVERY_ADDRESS',length=80))

db.define_table('product_info',
                Field('Reward_Name',length=20),
                Field('Reward_Value',length=20),
                Field('Reward_Points',length=20),
                Field('Reward_Internal_Cost',length=20),
                Field('product_id',length=20),
                Field('reserve_field',length=20))

db.define_table('user_info',
                Field('user_id',length=20),
                Field('user_name',length=20),
                Field('address',length=20),
                Field('mobilPhone',length=20),
                Field('passwd',length=20),
                Field('log_status',length=20)
                )

db.define_table('user2product',
                Field('product_id',length=20),
                Field('trials_count',length=20),
                Field('user_id',length=20),
                Field('reserve_field',length=20))
################ babybox CD BBS  ###################################################
db.define_table('correct_BCB',
                Field('order_id',length=20),
                Field('ex_id',length=20),
                Field('shop_name',length=20),
                Field('telephone',length=20),
                Field('cellphone',length=20),
                Field('user_name',length=20),
                Field('address',length=20),
                Field('province',length=20),
                Field('city',length=20),
                Field('county',length=20),
                Field('product_order',length=20),
                Field('barcode',length=20),
                Field('product_name',length=20),
                Field('product_size',length=20),
                Field('store_name',length=20),
                Field('store_size',length=20),
                Field('product_quantity',length=20))

db.define_table('incorrect_BCB',
                Field('order_id',length=20),
                Field('ex_id',length=20),
                Field('shop_name',length=20),
                Field('telephone',length=20),
                Field('cellphone',length=20),
                Field('user_name',length=20),
                Field('address',length=20),
                Field('province',length=20),
                Field('city',length=20),
                Field('county',length=20),
                Field('product_order',length=20),
                Field('barcode',length=20),
                Field('product_name',length=20),
                Field('product_size',length=20),
                Field('store_name',length=20),
                Field('store_size',length=20),
                Field('product_quantity',length=20),
                Field('wrong_reason',length=20),
                Field('status1',length=20)
                )

## after defining tables, uncomment below to enable auditing
auth.enable_record_versioning(db)
