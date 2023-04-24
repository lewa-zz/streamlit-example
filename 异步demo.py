import pprint
import asyncio
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright

baseurl = "https://gd.tzxm.gov.cn"
url = r"%s/PublicityInformation/PublicityHandlingResults.html#" % baseurl
apiurl = r"%s/tzxmspweb/api/publicityInformation/selectBaProjectInfo" % baseurl
post_data = {"baId": "1649223131300102146"}


# 普通请求类似于requets库
def pt_request():
    with sync_playwright() as p:
        context = p.request.new_context()
        response = context.get("https://example.com/user/repos")
        print(response.status)
        print(response.status_text)


# 浏览器请求
async def main(url, headers=None, img_path=None, handel_flow_func=None):
    async with async_playwright() as p:
        # for browser_type in [p.chromium, p.firefox, p.webkit]:        #可以指定任意三个浏览器
        browser_type = p.chromium
        browser = await browser_type.launch(
            headless=False
        )  # headless设置为False为显示打开的浏览器,slow_mo=50
        context = await browser.new_context(
            base_ulr=baseurl, ignore_https_errors=True
        )  # 解决net::ERR_CERT_COMMON_NAME_INVALID报错问题
        page = await context.new_page()
        # 如果指定监听函数的话
        if handel_flow_func:
            page.on("response", handel_flow_func)  # 监听浏览器中的response事件,获取加载的所有流量
            await page.wait_for_load_state("networkidle")
        # 设置请求头
        if headers:
            await page.set_extra_http_headers(headers=headers)
        await page.goto(url)
        # 如果指定截图保存路径的话
        if img_path:
            await page.screenshot(path=img_path)  # 保存截图
        get_title = await page.title()
        page_text = await page.content()
        print(get_title)
        # 关闭浏览器
        await context.close()
        await browser.close()
        # 判断需要获取的数据类型
        return {"Response": page_text, "Title": get_title}


# 封装获取html函数
def browser_request(url, headers=None, img_path=None, handel_flow_func=None):
    # html = asyncio.get_event_loop().run_until_complete(main(url, cookie))
    loop1 = asyncio.new_event_loop()
    asyncio.set_event_loop(loop1)
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(
        main(url, headers, img_path, handel_flow_func=handel_flow_func)
    )
    loop1.close()
    return data


# 用于监听浏览器的Responses事件
def on_response(response):
    print(f"Statue {response.status}:{response.url}")


if __name__ == "__main__":
    url = "https://www.baidu.com"
    data = browser_request(url=url, img_path="test.png", handel_flow_func=on_response)
    # print(data)
