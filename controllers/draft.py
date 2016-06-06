def class_by_size(title):
    if title =='12NB':
        return 'NN'
    elif title =='12S':
        return 'SS'
    elif title =='8NB':
        return 'N'
    elif title =='8S':
        return 'S'
    else:
        return ''

eps=0.00000000000000000000000000000001
all_application={'NN':0,'SS':0,'N':0,'S':0,'other':0}
good_application={'NN':0,'SS':0,'N':0,'S':0,'other':0}#status=3
dup_phone_application={'NN':0,'SS':0,'N':0,'S':0,'other':0}#phone duplication
dup_not_phone_application={'NN':0,'SS':0,'N':0,'S':0,'other':0}#not phone duplication
wrong_application={'NN':0,'SS':0,'N':0,'S':0,'other':0}#not phone duplication
#['oti_return']==1
good_app_rate={'NN':0,'SS':0,'N':0,'S':0,'other':0}# good_application/all_application*100%
daily_sum=sum(all_application.values())
good_sum=sum(good_application.values())
daily_rate=good_sum/(daily_sum+eps)

result=[]
def filter_count(**a_record):
    if a_record['shop_id']=='29':
        if a_record['status']==3:
            if a_record['product_title']=='12NB':
                pass
            elif a_record['product_title']=='12S':
                pass
            elif a_record['product_title']=='8NB':
                pass
            elif a_record['product_title']=='8S':
                pass
            else:
                pass
        elif a_record['status']==2:
            if a_record['wrong_reason']=='重复申领-SJ':
                if a_record['product_title']=='12NB':
                    pass
                elif a_record['product_title']=='12S':
                    pass
                elif a_record['product_title']=='8NB':
                    pass
                elif a_record['product_title']=='8S':
                    pass
                else:
                    pass
            elif '重复申领' in a_record['wrong_reason']:
                if a_record['product_title']=='12NB':
                    pass
                elif a_record['product_title']=='12S':
                    pass
                elif a_record['product_title']=='8NB':
                    pass
                elif a_record['product_title']=='8S':
                    pass
                else:
                    pass
            else:
                pass
        else:
            pass


    elif a_record['shop_id']=='108':
        pass
    elif a_record['shop_id']=='38':
        pass
    elif a_record['shop_id']=='103':
        pass
    else:
        pass















__author__ = 'Administrator'
