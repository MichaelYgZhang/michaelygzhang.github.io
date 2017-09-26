import urllib3
import json

if __name__ == '__main__':
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://www.baidu.com')
    print(r.status)
    print(r.data)
    print (r.headers)
    r = http.request('GET', 'http://httpbin.org/ip')
    print(json.loads(r.data.decode('utf-8')))