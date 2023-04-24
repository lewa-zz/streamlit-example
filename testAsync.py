import os
import asyncio
from playwright.async_api import async_playwright, Playwright


baseurl = "https://gd.tzxm.gov.cn"
url = r"%s/PublicityInformation/PublicityHandlingResults.html#" % baseurl
apiurl = "%s/tzxmspweb/api/publicityInformation/selectBaProjectInfo" % baseurl
post_data = {"baId": "1649223131300102146"}
current_json_result = ""


def on_response(response, url) -> None:
    """
    page on response的监听器,返回结束集
    """
    global current_json_result
    # 向接口提交的有api
    # r_headers =response.all_headers()
    # body= response.body()
    # beeprint.pp("response的头,其POSTDATA数据为了:%s" %r_headers)
    if apiurl in response.request.url and response.status == 200:
        # print("**********"+response.url)
        # current_json_result = response.json() #这个不能用,浅copy,不能这样返回,执行完,要深copy
        current_json_result = response.text()
        print(current_json_result)


async def run(playwright: Playwright):
    # This will launch a new browser, create a context and page. When making HTTP
    # requests with the internal APIRequestContext (e.g. `context.request` or `page.request`)
    # it will automatically set the cookies to the browser page and vice versa.
    browser = await playwright.chromium.launch()
    context = await browser.new_context(base_url="https://gd.tzxm.gov.cn")
    api_request_context = context.request
    page = await context.new_page()
    page.on("response", lambda response: on_response(response, url))
    # page.route(apiurl, handle_route)
    # Alternatively you can create a APIRequestContext manually without having a browser context attached:
    # api_request_context = await playwright.request.new_context(base_url="https://api.github.com")

    # Create a repository.

    response = await api_request_context.post(
        url,
        headers={
            "Accept-Encoding": "gzip",
            "Content-Type": "application/json;charset=utf-8",
            "Key": "332213fa4a9d4288b5668ddd9",
        },
        data=post_data,
    )

    print(response.json())
    print(response.text())
    assert response.ok
    assert response.json() != ""


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
