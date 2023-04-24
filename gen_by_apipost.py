import http.client

conn = http.client.HTTPSConnection("gd.tzxm.gov.cn")
payload = ""
headers = {
    "User-Agent": "apifox/1.0.0 (https://www.apifox.cn)",
    "Accept": "*/*",
    "Host": "gd.tzxm.gov.cn",
    "Connection": "keep-alive",
    "Content-Type": "application/json;charset=utf-8",
}
conn.request(
    "GET",
    "/PublicityInformation/resultDetail2.html?id=1649223131300102146&audit=ba&flag=gk&textShowFlag=undefined",
    payload,
    headers,
)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
