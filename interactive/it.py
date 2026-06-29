from utils import delay, fetch_with_backoff


def get_total_funds_investment(headers):
    data_acc = {"query": "acc", "nextId": 0, "instrumentTypes": "FUND"}
    url_acc = "https://api-prod.ii.co.uk/api/1/faceted-instrument-search-results?query=ord&nextId=0&instrumentTypes=INVESTMENT_TRUST"
    response = fetch_with_backoff(url_acc, headers=headers, data=data_acc)
    total = 0
    if response:
        output_acc = response.json()
        total = int(output_acc["other"]["total"])
    return total


def funds_investment(headers: dict) -> list[dict]:
    headers.update({"referer": "https://www.ii.co.uk/investment-trusts"})
    total = get_total_funds_investment(headers)
    print(f"[###] Total Investment found: {total} [###]")
    data = []
    for p in range(0, total, 3):
        print(f"[#] IF Funds [{p}-{p + 3}] out of {total}")
        query = {"query": "inc", "nextId": p, "instrumentTypes": "FUND"}
        response = fetch_with_backoff(
            f"https://api-prod.ii.co.uk/api/1/faceted-instrument-search-results?query=ord&nextId={p}&instrumentTypes=INVESTMENT_TRUST",
            headers=headers,
            data=query,
        )
        if response:
            output = response.json()
            funds = output["other"]["results"]
            for fund in funds:
                name = fund["name"].replace("Ord", "")
                url = f"https://www.ii.co.uk{fund['urlId']}"
                isin = fund["isin"]
                data.append(dict(name=name, isin=isin, url=url))
            delay(1.5, 3)
    return data
