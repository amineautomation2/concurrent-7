from pprint import pprint
from random import uniform
from time import sleep
import requests
import openpyxl
from utils import fetch_with_backoff, setup_driver, delay, write_json


def get_total_funds_mf(headers) -> dict:
    data_acc = {
        "query": "acc",
        "nextId": 0,
        "instrumentTypes": "FUND"
    }
    data_inc = {
        "query": "inc",
        "nextId": 0,
        "instrumentTypes": "FUND"
    }
    headers.update({"referer": "https://www.ii.co.uk/funds", })
    url_acc = 'https://api-prod.ii.co.uk/api/1/faceted-instrument-search-results?query=acc&nextId=0&instrumentTypes=FUND'
    url_inc = "https://api-prod.ii.co.uk/api/1/faceted-instrument-search-results?query=inc&nextId=0&instrumentTypes=FUND"
    response_acc = fetch_with_backoff(url_acc, headers=headers, data=data_acc)
    delay(0.5, 1)
    response_inc = fetch_with_backoff(url_inc, headers=headers, data=data_inc)
    total_inc = 0
    total_acc = 0
    if response_inc:
        output_inc = response_inc.json()
        total_inc = int(output_inc["fund"]["total"])
    if response_acc:
        output_acc = response_acc.json()
        total_acc = int(output_acc["fund"]["total"])

    return {"acc": total_acc,
            "inc": total_inc}


def funds_mf(headers: dict, total: int, type: str) -> list[dict]:
    headers.update({"referer": "https://www.ii.co.uk/funds", })
    print(f'[###] Total {type.capitalize()} MF: {total} [###]')
    data = []
    for p in range(0, total, 3):
        print(f'[#] MF Funds [{p}-{p + 3}] out of {total}')
        query = {"query": type,
                 "nextId": p,
                 "instrumentTypes": "FUND"}
        response = fetch_with_backoff(
            f'https://api-prod.ii.co.uk/api/1/faceted-instrument-search-results?query={type}&nextId={p}&instrumentTypes=FUND', headers=headers, data=query)
        if response:
            output = response.json()
            # write_json("inter.json", output)
            funds = output["fund"]["results"]
            for fund in funds:
                for f in fund["results"]:
                    name = f["name"]
                    url = f'https://www.ii.co.uk{f["urlId"]}'
                    isin = f["isin"]
                    data.append(dict(name=name, isin=isin, url=url))
        sleep(uniform(0.5, 1.5))
    return data
