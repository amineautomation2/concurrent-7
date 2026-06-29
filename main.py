import argparse
import time

from interactive import get_urls, interactive_runner
from utils import create_spreadsheet, get_xlsx_filepath
from worker import merge_csv_to_xlsx


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=str, help="id worker")
    parser.add_argument("--max", type=str, help="max worker")
    parser.add_argument("--sheet", type=str, help="sheet name")
    parser.add_argument("--url", action="store_true", help="get funds url")
    parser.add_argument("--fresh", action="store_true", help="create fresh spreadsheet")
    parser.add_argument("--merge", action="store_true", help="merge csvs")
    args = parser.parse_args()

    # with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
    #    print(f"email_title={email_title()}", file=fh)
    xlsx_out = get_xlsx_filepath("interactive_investor.xlsx")

    if args.fresh:
        create_spreadsheet(
            xlsx_out, ["Investment", "ETF", "MF"], ["Name", "ISIN", "URL", "Keyword"]
        )

    elif args.url:
        get_urls(args.sheet)

    elif args.id and args.max and args.sheet:
        interactive_runner(
            id_worker=int(args.id), max_worker=int(args.max), sheet=args.sheet
        )

    elif args.merge and args.sheet:
        merge_csv_to_xlsx(xlsx_out, ["name", "isin", "url", "keyword"], args.sheet)
    else:
        print("No arguments found.")


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    # s = [
    #    {
    #        "name": "Scottish Mortgage",
    #        "isin": "GB00BLDYK618",
    #        "url": "https://www.ii.co.uk/investment-trusts/scottish-mortgage-ord/LSE:SMT",
    #    }
    # ]
    # with sync_playwright() as p:
    #    # Pass 'p' and your list of funds. Adjust batch_size lower if runner memory is very tight.
    #    scraped_data = get_funds_keywords_playwright(p, s, batch_size=40)
    #    print(scraped_data)
    elapsed_time = time.perf_counter() - start_time
    print(f"Execution time: {elapsed_time:.2f} seconds")
