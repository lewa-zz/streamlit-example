from playwright.sync_api import sync_playwright
from prefect import task, flow, get_run_logger

@task(name="页面加载", 
      retries=3, retry_delay_seconds=2,description="Get the Data by request")
def load_page(context, href: str):
    # Open new page
    page = context.new_page()
    r = page.goto(href)
    if r.status != 200:
        raise Exception("页面加载失败，重试中！")
    return page
    

@flow(flow_run_name="从EXCEL读出拉页面")
def my_flow(name: str, pagenu: int ):
    logger = get_run_logger()
    logger.info('%s 第%d页启动'%(name,pagenu))
    browser = load_page(pagenu,"")
    
    

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        href = 'https://ygp.gdzwfw.gov.cn/zjfwcs/gd-zjcs-pub/bidResultNotice/view/4419001257480170562212270347'
        page = load_page(context,href)
        t= page.locator("//html/body/div/div[2]/p")
        t.text_content()
        print(t)
        context.close()
        browser.close()


def run(playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    #browser = playwright.chromium.launch()
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # page.on("request", lambda request: print(request.url))
    page.on("response", res)

    # Go to
    page.goto("https://ygp.gdzwfw.gov.cn/zjfwcs/gd-zjcs-pub/bidResultNotice")


    # ---------------------
    context.close()
    browser.close()

def res(res) -> None:
    if "id" in res.url:
        print("**********"+res.url)

def tryit(s:str):
    
# with sync_playwright() as playwright:
#     run(playwright)
def load_page():
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    href = 'https://ygp.gdzwfw.gov.cn/zjfwcs/gd-zjcs-pub/bidResultNotice/view/4419001257480170562212270347'
    page = context.new_page()
    page.goto(href)
    t= page.locator("//html/body/div[4]/div[2]/div[2]/ul/li[5]/div")
    t.inner_text()
    print(t)
    context.close()
    browser.close()

load_page()
#my_flow("dg",0)