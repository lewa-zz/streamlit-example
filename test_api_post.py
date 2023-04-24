#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    :   test_api_post.py
@Time    :   2023/04/21 23:39:09
@Author  :   Rico Chen 
@Mail    :   55059@qq.com
@Version :   1.0
@Desc    :   None
"""

import os
from playwright.sync_api import sync_playwright


baseurl = "https://gd.tzxm.gov.cn"
# url = href if href != "" else r"%s/PublicityInformation/PublicityHandlingResults.html#" % baseurl
apiurl = "%s/tzxmspweb/api/publicityInformation/selectBaProjectInfo" % baseurl
post_data = {"baId": "1649223131300102146"}
# apiurl = r"%s/tzxmspweb/api/publicityInformation/selectByPageBA" % baseurl
# weburl = r"/PublicityInformation/PublicityHandlingResults.html#"

# post_data = {
#     "city": "4419",
#     "flag": "1",
#     "nameOrCode": "",
#     "pageNumber": 1,
#     "pageSize": 15,
# }
with sync_playwright() as p:
    # This will launch a new browser, create a context and page. When making HTTP
    # requests with the internal APIRequestContext (e.g. `context.request` or `page.request`)
    # it will automatically set the cookies to the browser page and vice versa.
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(base_url=baseurl)
    api_request_context = context.request
    page = context.new_page()  # api_request_context
    response = page.request.post(
        apiurl,
        headers={
            "Accept-Encoding": "gzip",
            "Content-Type": "application/json;charset=utf-8",
            "Key": "332213fa4a9d4288b5668ddd9",
        },
        data=post_data,
    )
    print(response.text())
    print(response.json())
