import hashlib
import urllib
import random
import json
import Translator.api as api


class Baidu(object):
    def __init__(self, **kw):
        self.appid = kw['appid']
        self.key = kw['key']
        self.enabled = kw['enabled']

    def set_appid(self, appid):
        self.appid = str(appid)

    def set_key(self, key):
        self.key = str(key)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def translate(self, text):
        print("call")
        appid = self.appid
        secretKey = self.key
        host='api.fanyi.baidu.com'
        myurl = '/api/trans/vip/translate'
        fromLang = 'auto'   #原文语种
        toLang = 'zh'       #译文语种
        salt = random.randint(32768, 65536)
        q = text
        sign = appid + q + str(salt) + secretKey
        sign = hashlib.md5(sign.encode()).hexdigest()
        myurl = myurl \
                + '?appid=' + appid \
                + '&q=' + urllib.parse.quote(q) \
                + '&from=' + fromLang \
                + '&to=' + toLang \
                + '&salt=' + str(salt) \
                + '&sign=' + sign
        response = api.get(host,myurl)
        return processResponse(response)


def errormap(code):
    MAPPING = {
        '52003': "Error:52003 | APP ID或密钥错误",
        '54003': "Error:54003 | 请求过快，你看得似乎有点快",
        '54004': "Error:54004 | 账户余额不足",
        '54005': "Error:54005 | 文本过长",
        '58000': "Error:58000 | 客户端IP非法，请检查百度翻译后台-个人资料中的'IP地址限制'",
        '58002': "Error:58002 | 翻译服务已经关闭，请前往'管理控制台'开启",
        '90107': "Error:90107 | 实名认证未通过或未生效",
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
        code = res['error_code'] # 获取错误信息
        return errormap(code) # 
    except Exception:
        return res['trans_result'][0]['dst'] # 返回翻译结果