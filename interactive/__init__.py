from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from utils import setup_driver, get_random_user_agent, find_element_or_none, delay, get_xlsx_filepath, get_with_backoff
from .it import funds_investment
from .etf import funds_etf
from .mutual_fund import funds_mf, get_total_funds_mf
from openpyxl import load_workbook


def get_funds_keywords(driver: WebDriver, funds: list[dict]) -> list[dict]:
    data = []
    wait = WebDriverWait(driver, timeout=5)
    for fund in funds:
        url = fund["url"]
        get_with_backoff(driver, url)
        print(f"current url: {url}")
        keyword_xpath = '//div[@data-testid="allowedaccounts"]/p'
        keyword_elm = find_element_or_none(wait, keyword_xpath)
        keyword = None
        if keyword_elm:
            keyword = keyword_elm.text.strip()
        f = dict(name=fund["name"], isin=fund["isin"],
                 url=fund["url"], keyword=keyword)
        data.append(f)
        delay(2, 3)
    return data


def write_spreadsheet(filepath: str, sheet: str, data: list[dict]) -> None:
    wb = load_workbook(filepath)
    ws = wb[sheet]
    i = 2
    for f in data:
        ws.cell(i, 1, f["name"])
        ws.cell(i, 2, f["isin"])
        cell = ws.cell(i, 3, f["url"])
        cell.style = "Hyperlink"
        cell.hyperlink = f["url"]
        ws.cell(i, 4, f["keyword"])
        i += 1
    wb.save(filepath)
    wb.close()


def interactive_runner(sheet: str):
    driver = setup_driver(True)
    driver.set_page_load_timeout(30)
    headers = {
        "accept": "application/json;charset=UTF-8",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US, en;q=0.9,fr-FR;q=0.8,fr;q=0.7",
        "cache-control": "no-cache",
        "ii-consumer-type": "web.public",
        "origin": "https://www.ii.co.uk",
        "pragma": "no-cache",
    }
    xlsx_path = get_xlsx_filepath("interactive_investor.xlsx")
    if sheet == "Investment":
        ua = get_random_user_agent()
        headers.update(ua)
        it_data = funds_investment(headers)
        it_data = get_funds_keywords(driver, it_data)
        write_spreadsheet(xlsx_path, "Investment", it_data)

    if sheet == "ETF":
        ua = get_random_user_agent()
        headers.update(ua)
        etf_data = funds_etf(headers)
        etf_data = get_funds_keywords(driver, etf_data)
        write_spreadsheet(xlsx_path, "ETF", etf_data)

    if sheet == "MF":
        ua = get_random_user_agent()
        headers.update(ua)
        total_mf = get_total_funds_mf(headers)
        total_inc = total_mf["inc"]
        total_acc = total_mf["acc"]
        mf_data_inc = funds_mf(headers, total_inc, "inc")
        mf_data_inc = get_funds_keywords(driver, mf_data_inc)

        mf_data_acc = funds_mf(headers, total_acc, "acc")
        mf_data_acc = get_funds_keywords(driver, mf_data_acc)
        mf_data = mf_data_inc + mf_data_acc
        write_spreadsheet(xlsx_path, "MF", mf_data)


def funds_dedup(funds: list[dict]) -> list[dict]:
    seen = set()
    dedup = [d for d in funds if tuple(
        d.items()) not in seen and not seen.add(tuple(d.items()))]
    return dedup
