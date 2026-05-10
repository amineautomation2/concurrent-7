from pprint import pprint
from random import uniform
from time import sleep
import requests
import openpyxl
from utils import setup_driver, delay, write_json


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
    url_acc = f'https://api-prod.ii.co.uk/api/1/faceted-instrument-search-results?query=acc&nextId=0&instrumentTypes=FUND'
    url_inc = f"https://api-prod.ii.co.uk/api/1/faceted-instrument-search-results?query=inc&nextId=0&instrumentTypes=FUND"
    response_acc = requests.get(url_acc, headers=headers, data=data_acc)
    delay(0.5, 1)
    response_inc = requests.get(url_inc, headers=headers, data=data_inc)
    output_acc = response_acc.json()
    output_inc = response_inc.json()

    return {"acc": int(output_acc["fund"]["total"]),
            "inc": int(output_inc["fund"]["total"])}


def funds_mf(headers: dict, total: int, type: str) -> list[dict]:
    headers.update({"referer": "https://www.ii.co.uk/funds", })
    print(f'[###] Total {type.capitalize()} MF: {total} [###]')
    data = []
    for p in range(0, total, 3):
        print(f'[#] MF Funds [{p}-{p + 3}] out of {total}')
        query = {"query": type,
                 "nextId": p,
                 "instrumentTypes": "FUND"}
        response = requests.get(
            f'https://api-prod.ii.co.uk/api/1/faceted-instrument-search-results?query={type}&nextId={p}&instrumentTypes=FUND', headers=headers, data=query)
        output = response.json()
        # write_json("inter.json", output)
        funds = output["fund"]["results"]
        for fund in funds:
            for f in fund["results"]:
                name = f["name"]
                url = f'https://www.ii.co.uk{f["urlId"]}'
                isin = f["isin"]
                data.append(dict(name=name, isin=isin, url=url))
        sleep(uniform(0.3, 0.5))
    return data
