import urllib3
import json
import sys
import certifi


print("defaultencoding:"+sys.getdefaultencoding())

if __name__ == '__main__':
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    # r = http.request_encode_url('GET', 'https://movie.douban.com/subject/27038183/?from=showing')
    # print(r.status)
    # print(r.data)
    # print (r.headers)
    #
    # r = http.request('GET', 'http://httpbin.org/ip')
    # json.loads(r.data.decode('utf-8'))

# http://www.douban.com/tag/名著/book?start=0   url 中文问题待解决

    r = http.request('GET', 'http://8.lemicp.com/trade/jczq/hhtz?playid=9006&e=2')
    print(r.status)

    r = http.request('GET', 'https://book.douban.com/')
    print(r.data)

