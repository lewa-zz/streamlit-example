import json

import requests
import random

random_int = random.randint(0, 14)
# get_cookie_url = 'https://gd.tzxm.gov.cn/PublicityInformation/PublicityHandlingResultsList.html'
get_cookie_url = 'https://gd.tzxm.gov.cn/tzxmspweb/api/publicityInformation/selectByPageBA'
# get_cookie_url = 'https://gd.tzxm.gov.cn/PublicityInformation/PublicityHandlingResults.html'


get_data_url = 'https://gd.tzxm.gov.cn/tzxmspweb/api/publicityInformation/selectByPageBA'
# get_data_url = 'https://gd.tzxm.gov.cn/tzxmspweb/api/publicityInformation/selectAdmdiv'
user_agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36 OPR/37.0.2178.32",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 BIDUBrowser/8.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.277.400 QQBrowser/9.4.7658.400",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 UBrowser/5.6.12150.8 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36 SE 2.X MetaSr 1.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) Gecko/20100101 Firefox/60.0"
]
headers = {
    'user-agent': user_agent[random_int],
    # 'Content-Type': 'application/json;charset=UTF-8'
}
session_cookies = requests.get(get_cookie_url, headers=headers).cookies.get_dict()
print(session_cookies)

params = {
    # "city": "",
    "flag": "1",
    # "nameOrCode": "",
    "pageNumber": 1,
    "pageSize": 15,
}

# params = {"symbol": "HKHSTECH", "begin": "1667794762000", "period": "day",
#           "count": "-3","indicator": "kline,pe,pb,ps,pcf,market_capital,agt,balance"}
res = requests.post(
    url=get_data_url,
    headers=headers,
    cookies=session_cookies,
    # data=json.dumps(params),
    # data=params,
    json=params,
    # auth=None,
    verify=False
)
print(res.text)
