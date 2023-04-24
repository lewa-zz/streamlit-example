import asyncio
from playwright.async_api import async_playwright

base_url = "https://gd.tzxm.gov.cn"
# res_url = r"%s/PublicityInformation/PublicityHandlingResults.html#" % base_url
# api_url = r"%s/tzxmspweb/api/publicityInformation/selectBaProjectInfo" % base_url
# post_data = {"baId": "1649223131300102146"}

res_url = r"%s/PublicityInformation/PublicityHandlingResults.html#" % base_url
api_url = r"%s/tzxmspweb/api/publicityInformation/selectByPageBA" % base_url


async def on_response(response, url) -> None:
    """
    page on response的监听器,返回结束集的
    """
    # 向接口提交的有api
    # r_headers =response.all_headers()
    # body= response.body()
    # beeprint.pp("response的头,其POSTDATA数据为了:%s" %r_headers)
    if "selectByPageBA" in response.request.url and response.status == 200:
        current_json_result = response.text()
        print("**********" + current_json_result)  # response.url)
    # self.current_json_result = response.json() #这个不能用,浅copy,不能这样返回,执行完,要深copy
    # self.current_json_result = response.text()


async def run(url):
    async with async_playwright() as playwright:
        chromium = playwright.chromium
        browser = await chromium.launch(headless=False)
        # create two isolated browser contexts
        user_context = await browser.new_context(base_url=base_url)
        page = await user_context.new_page()
        page.on("response", lambda response: on_response(response, url))
        await page.goto(url)
        # await page2.goto('https://www.baidu.com')


async def main():
    tasks = []
    urls = [
        res_url,
    ]
    for url in urls:
        task = asyncio.ensure_future(run(url))
        tasks.append(task)
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
