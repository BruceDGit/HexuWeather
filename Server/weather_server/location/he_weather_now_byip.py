
#python
import json,urllib
from urllib import parse
from urllib.request import urlopen



url = 'https://free-api.heweather.net/s6/weather/now'
params = {
    'location': '%s'%input('请输入ip地址：'),
    'lang': 'zh-Hans',
    'unit': 'm',
    'key':'4dcf0ac571c64e45ad7767a44f692902'
}
params = urllib.parse.urlencode(params)


f = urlopen('%s?%s' % (url, params))
nowapi_call = f.read()
#print content
a_result = json.loads(nowapi_call)
djson=json.dumps(a_result,ensure_ascii=False)
# print(djson)
def jsonFile(fileData):
	file = open("weather_ip.json","w")
	file.write(fileData)
	file.close()

if __name__ == '__main__':

    jsonFile(djson)