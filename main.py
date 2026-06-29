import argparse
import time

from interactive import interactive_runner


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sheet", type=str, help="Fund type")

    args = parser.parse_args()

    if args.sheet:
        interactive_runner(args.sheet)
    # with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
    #    print(f"email_title={email_title()}", file=fh)


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
