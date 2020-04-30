import http.client

# 发送请求
def post(host, url, body, headers):
    httpClient = None
    try:
        httpClient = http.client.HTTPSConnection(host)
        httpClient.request('POST', url, body, headers)
        response = httpClient.getresponse()
        return response.read()
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()

def get(host, url):
    try:
        httpClient = http.client.HTTPSConnection(host)
        httpClient.request('GET', url)
        response = httpClient.getresponse()
        return response.read()
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()
