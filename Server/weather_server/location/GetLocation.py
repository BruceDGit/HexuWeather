"""
    根据IP地址查询归属地
"""
import json,urllib
from urllib import parse
from urllib.request import urlopen


class GetLocation(object):
    def __init__(self, ip_addr):
        self.url = 'http://api.k780.com'
        self.params_dict = {
          'ip': ip_addr,
          'appkey' : '45087',
          'sign'   : 'b998899107bb97b807597ff308f2ea19',
          'format' : 'json'
        }
        self.params = urllib.parse.urlencode(self.params_dict)

    def result(self):
        f = urlopen('%s?app=ip.get&%s' % (self.url , self.params))
        nowapi_call = f.read()
        a_result = json.loads(nowapi_call)
        res = a_result["result"]["att"]
        if res.count(',') == 1:
            res = res + ',' + res.split(',')[1]
        return res


if __name__ == '__main__':
    req = GetLocation('106.47.42.62')
    print(req.result())
