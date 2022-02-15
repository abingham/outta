import argparse
from outta.parser import Parser


def explain(filename):
    "Print explanation of elements in text."
    with open(filename, mode="rt") as handle:
        text = handle.read()

    parser = Parser()
    elements = tuple(parser.feed(text))
    for element in elements:
        print(element)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("FILE")
    args = parser.parse_args()
    explain(args.FILE)


if __name__ == "__main__":
    main()
