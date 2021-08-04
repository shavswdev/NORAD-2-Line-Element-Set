import urllib3

http = urllib3.PoolManager() #PoolManager necessary to handle requests

url_target = "http://www.celestrak.com/NORAD/elements/stations.txt"

sleep(5)

nLineNum = 0

print(urllib3.__version__)

for line in http.request('GET', url_target):
    print (line)
    nLineNum += 1

print (nLineNum)

