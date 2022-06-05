import http.client
import json
import math

from authserver import app
from authserver.transformers.order_data_csv_transformer import calculate_discount
from secrets import secrets


def send_email(template_id, payload_data):
    try:
        conn = http.client.HTTPConnection("api.msg91.com")
        payload = {
            **payload_data['variables'],
            "authkey": secrets['EMAIL_AUTH_KEY'],
            "template_id": template_id,
            "to": {
                "email": payload_data['to_email']
            },
            "from": {
                "email": 'support@basickart.com'
            },
            "domain": "basickart.com",
            "mail_type_id": "1"
        }

        headers = {'content-type': 'application/json'}
        conn.request('POST', '/api/v5/email', json.dumps(payload), headers)
        print(payload)
        res = conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))
        conn.close()

    except Exception as e:
        conn.close()
        app.logger.debug(e)


def customer_order_details_helper(productData):
    product_tr = '<tr> <td width="80%" class="purchase_item" style="word-break: break-word; font-family: &quot;Nunito ' \
         'Sans&quot;, Helvetica, Arial, sans-serif; font-size: 15px; color: #51545E; line-height: 18px; padding: 10px ' \
         '0;"> ' \
         '<span class="f-fallback">{productName}</span></td> ' \
         '<td class="align-right" width="20%" style="word-break: break-word; font-family: &quot;Nunito Sans&quot;, ' \
         'Helvetica, Arial, sans-serif; font-size: 16px; text-align: right;" align="right">' \
         ' <span class="f-fallback">{productPrice}</span></td></tr>'
    discount_tr = '<tr><td width="80%" class="purchase_footer" valign="middle" style="word-break: break-word; ' \
                  'font-family: &quot;Nunito Sans&quot;, Helvetica, Arial, sans-serif; font-size: 16px; ' \
                  'padding-top: 15px; border-top-width: 1px; border-top-color: #EAEAEC; border-top-style: solid;">' \
                  '<p class="f-fallback purchase_total purchase_total--label" style="font-size: 16px; ' \
                  'line-height: 1.625; text-align: right; font-weight: bold; color: #333333; margin: 0; ' \
                  'padding: 0 15px 0 0;" align="right">Discount</p></td>' \
                  '<td width="20%" class="purchase_footer" valign="middle" style="word-break: break-word; ' \
                  'font-family: &quot;Nunito Sans&quot;, Helvetica, Arial, sans-serif; font-size: 16px; ' \
                  'padding-top: 15px; border-top-width: 1px; border-top-color: #EAEAEC; border-top-style: solid;">' \
                  '<p class="f-fallback purchase_total" style="font-size: 16px; line-height: 1.625; ' \
                  'text-align: right; font-weight: bold; color: #333333; margin: 0;" align="right">' \
                  '{discountPercentage}' \
                  '</p></td></tr>'
    result_tr = ''
    total_amount = 0
    discount_rate = ''

    for product_obj in productData:
        total_amount += math.ceil(int(product_obj['totalamount']))
        result_tr += product_tr.format(productName=product_obj['productname'],
                                       productPrice=str(math.ceil(int(product_obj['totalamount']))))
    total_amount = calculate_discount(int(total_amount),
                                   int(productData[0]['userdiscount']) if productData[0]['userdiscount'] else None,
                                   int(productData[0]['coupondiscount']) if productData[0]['coupondiscount'] else None)

    if productData[0]['userdiscount'] and productData[0]['coupondiscount']:
        discount_rate = str(productData[0]['userdiscount']) + '% + ' + str(productData[0]['coupondiscount']) + '%'
    elif productData[0]['userdiscount']:
        discount_rate = str(productData[0]['userdiscount']) + '%'
    elif productData[0]['coupondiscount']:
        discount_rate = str(productData[0]['coupondiscount']) + '%'

    if discount_rate != '':
        discount_tr = discount_tr.format(discountPercentage=discount_rate)
    else:
        discount_tr = ''
    return {
        'total_amount': total_amount,
        'product_list': result_tr,
        'discount_tr': discount_tr
    }
