import json
import Translator.api as api

class Caiyun(object):
    def __init__(self, **kw):
        self.token = kw['token']
        self.enabled = kw['enabled']

    def set_token(self, token):
        self.token = token

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def translate(self, text):
        if self.enabled:
            token = self.token
            host = 'api.interpreter.caiyunai.com'
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
            response = api.post(host, myurl, json.dumps(payload), headers)
            return processResponse(response)

def errormap(code):
    MAPPING = {
        'API rate limit exceeded': "请求速度过快",
        'Invalid token': "token输入错误",
    }
    try:
        s = MAPPING[code]
        return s
    except Exception:
        return code

def processResponse(res):
    
    try:
        res = json.loads(res) # 转换成json对象
    except Exception:
        return "未知数据错误"
    try:
        err = res['message'] # 获取错误信息
        return errormap(err)
    except Exception:
        try:
            return res['target'] # 返回翻译结果
        except Exception:
            return "未知错误2"