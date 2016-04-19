__author__ = 'Administrator'
'''
data={"order_id":vars['out_tid']}
    order_phone=db().select(db.trade.mobilPhone).as_list()
    if not {'mobilPhone':content['mobilPhone']} in order_phone:
        data["status"]=3
        db.trade.insert(**content)
    else:
        data["status"]=2
        data["message"]='duplicated trade order'
    updateTOS(data)
    AddTrade(data)

AllBarcode=db().select(db.AllBarcode.bar_code).as_list()
({'bar_code':vars['product_info'][0]['barCode']} in AllBarcode)
    data={"order_id":vars['out_tid']}
                if not {'mobilPhone':content['mobilPhone']} in order_phone:
                    data["status"]="3"
                    order_state['status']=3
                else:
                    data["status"]="2"
                    order_state['status']=2
                    data["message"]='duplicated trade order'
                updateTOS(data)
                AddTrade(edbdata)
            else:
                msg.append({'is_success':'false','response_Msg':'wrong identifier params sig or barCode'})
            db(db.trade.id==getorderid).select().first().update_record(status=order_state['status'])
                order_phone=db().select(db.trade.mobilPhone).as_list()
'''






















