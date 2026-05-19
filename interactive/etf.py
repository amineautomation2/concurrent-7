import requests

import openpyxl
from utils import setup_driver, delay, fetch_with_backoff


def get_total_funds_etf(headers: dict):
    data_acc = {
        "query": "acc",
        "nextId": 0,
        "instrumentTypes": "FUND"}
    url_acc = 'https://api-prod.ii.co.uk/api/1/faceted-instrument-search-results?query=etf&nextId=0&instrumentTypes=ETF'
    response = fetch_with_backoff(url_acc, headers=headers, data=data_acc)
    if response:
        output_acc = response.json()
        return int(output_acc["other"]["total"])
    return 0


def funds_etf(headers: dict):
    headers.update({"referer": "https://www.ii.co.uk/etfs"})
    total = get_total_funds_etf(headers)
    print(f'[###] Total ETF found: {total} [###]')
    data = []
    for p in range(0, total, 3):
        print(f'[#] ETF Funds [{p}-{p + 3}] out of {total}')
        query = {"query": "inc",
                 "nextId": p,
                 "instrumentTypes": "FUND"}
        response = fetch_with_backoff(
            f'https://api-prod.ii.co.uk/api/1/faceted-instrument-search-results?query=etf&nextId={p}&instrumentTypes=ETF', headers=headers, data=query)
        if response:
            output = response.json()
            funds = output["other"]["results"]
            for fund in funds:
                name = fund["name"].replace('Ord', '')
                url = f'https://www.ii.co.uk{fund["urlId"]}'
                isin = fund["isin"]
                data.append(dict(name=name, isin=isin, url=url))
            delay(0.5, 1.5)
    return data
