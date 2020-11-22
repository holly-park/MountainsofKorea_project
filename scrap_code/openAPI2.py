from urllib.request import urlopen
from urllib.parse import urlencode,unquote,quote_plus
import urllib

url = 'http://apis.data.go.kr/1400000/service/cultureInfoService'

queryParams = '?' + urlencode({ quote_plus('servicekey') : 'cRhBhi3sxVClCIks%2FemvBBGZgcYv5HaKvFr26Ov5Q5nor0WtrgUNO9rwfYO6FkLUif9SefP0BK%2B18mBFvV8%2FCw%3D%3D',
                                quote_plus('searchWrd') : u'북한산' })

request = urllib.request.Request(url+unquote(queryParams))
print ('Your Request:\n'+url+queryParams)
request.get_method = lambda: 'GET'
response_body = urlopen(request).read()
print ("\nResult:")
print (response_body)
print ("\nDataType of Result Data:")
print (type(response_body))