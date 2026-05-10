import time
from interactive import interactive_runner
import argparse


def main() -> None:
    start_time = time.perf_counter()
    parser = argparse.ArgumentParser()
    parser.add_argument("--sheet", type=str, help="Fund type")

    args = parser.parse_args()

    if args.sheet:
        interactive_runner(args.sheet)
    # with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
    #    print(f"email_title={email_title()}", file=fh)
    elapsed_time = time.perf_counter() - start_time
    print(f"Execution time: {elapsed_time:.2f} seconds")


if __name__ == "__main__":
    main()
