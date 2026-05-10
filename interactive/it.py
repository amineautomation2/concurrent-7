from random import uniform
from time import sleep
import requests
import openpyxl
from utils import setup_driver, delay


def get_total_funds_investment(headers):
    data_acc = {
        "query": "acc",
        "nextId": 0,
        "instrumentTypes": "FUND"}
    url_acc = f'https://api-prod.ii.co.uk/api/1/faceted-instrument-search-results?query=ord&nextId=0&instrumentTypes=INVESTMENT_TRUST'
    response = requests.get(url_acc, headers=headers, data=data_acc)
    output_acc = response.json()
    return int(output_acc["other"]["total"])


def funds_investment(headers: dict) -> list[dict]:
    headers.update({"referer": "https://www.ii.co.uk/investment-trusts"})
    total = get_total_funds_investment(headers)
    print(f'[###] Total Investment found: {total} [###]')
    data = []
    for p in range(0, total, 3):
        print(f'[#] IF Funds [{p}-{p + 3}] out of {total}')
        query = {"query": "inc",
                 "nextId": p,
                 "instrumentTypes": "FUND"}
        response = requests.get(
            f'https://api-prod.ii.co.uk/api/1/faceted-instrument-search-results?query=ord&nextId={p}&instrumentTypes=INVESTMENT_TRUST', headers=headers, data=query)
        output = response.json()
        funds = output["other"]["results"]
        for fund in funds:
            name = fund["name"].replace('Ord', '')
            url = f'https://www.ii.co.uk{fund["urlId"]}'
            isin = fund["isin"]
            data.append(dict(name=name, isin=isin, url=url))
        delay(0.3, 0.5)
    return data
