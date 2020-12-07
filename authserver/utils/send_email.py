import http.client
import json

from authserver import app
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

