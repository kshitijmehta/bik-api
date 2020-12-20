import http.client
import json

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
            "to": payload_data['to_email'],
            "from": 'support@basickart.com',
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
    tr = '<tr> <td width="80%" class="purchase_item" style="word-break: break-word; font-family: &quot;Nunito ' \
         'Sans&quot;, Helvetica, Arial, sans-serif; font-size: 15px; color: #51545E; line-height: 18px; padding: 10px ' \
         '0;"> ' \
         '<span class="f-fallback">{productName}</span></td> ' \
         '<td class="align-right" width="20%" style="word-break: break-word; font-family: &quot;Nunito Sans&quot;, ' \
         'Helvetica, Arial, sans-serif; font-size: 16px; text-align: right;" align="right">' \
         ' <span class="f-fallback">{productPrice}</span></td></tr>'
    result_tr = ''
    total_amount = 0
    for product_obj in productData:
        product_price = calculate_discount(int(product_obj['totalamount']),
                                           int(product_obj['userdiscount']) if product_obj['userdiscount'] else None,
                                           int(product_obj['coupondiscount']) if product_obj[
                                               'coupondiscount'] else None)
        total_amount += int(product_price)
        result_tr += tr.format(productName=product_obj['productname'], productPrice=str(product_price))
    return {
        'total_amount': total_amount,
        'product_list': result_tr
    }
