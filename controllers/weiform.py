# -*- coding: utf-8 -*-

def taobao():
    form_content={}
    if request.vars.name:
        form_content['consignee']=request.vars.name
    if request.vars.phonecall:
        form_content['mobilPhone']=request.vars.phonecall
    if request.vars.province:
        form_content['province']=request.vars.province
    if request.vars.city:
        form_content['city']=request.vars.city
    if request.vars.address:
        form_content['address']=request.vars.address

    esskey=['consignee','mobilPhone','province','city','address']
    ret={}
    if set(form_content.keys()) >= set(esskey):
        pid=db.weitrade.insert(**form_content)
        ret['result']='submit successfully'
    else:
        ret['result']='wrong'
        ret['wrong_reason']='abcense of field'
    return ret




