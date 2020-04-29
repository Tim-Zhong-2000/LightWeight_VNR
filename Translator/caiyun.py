import http.client
import json

def res2json(response):
    return json.loads(response.read().decode("utf-8"))

def errorhandel(code):
    MAPPING = {
        'API rate limit exceeded': "请求速度过快",
        'Invalid token': "token输入错误",
    }
    try:
        s = MAPPING[code]
        return s
    except Exception:
        return "未知错误"

class Caiyun(object):
    def __init__(self, **kw):
        self.token = kw['token']
        self.enabled = False

    def set_token(self, token):
        self.token = token

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def translate(self, text):
        if self.enabled:
            token = self.token
            httpClient = None
            myurl = '/v1/translator'
            direction = "auto2zh"
            headers = {
                'content-type': "application/json",
                'x-authorization': "token " + token,
            }
            payload = {
                "source": text,
                "trans_type": direction,
                "request_id": "demo",
                "detect": True,
            }
            try:
                httpClient = http.client.HTTPConnection(
                    'api.interpreter.caiyunai.com')
                httpClient.request('POST', myurl, json.dumps(payload), headers)
                response = httpClient.getresponse()
                if response.code == 200:
                    res = res2json(response)
                    return res['target']
                if response.code == 403:
                    res = res2json(response)
                    return errorhandel(res['message'])
                return "未知错误"
            except Exception as e:
                print(e)
            finally:
                if httpClient:
                    httpClient.close()
