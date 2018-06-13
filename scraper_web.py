from pickle import load
from time import ctime
from pprint import pprint


def load_results(file='scraper_results.store') -> dict:
    with open(file, 'rb') as f:
        return load(f)

if __name__ == '__main__':
    pprint(f"Last updated: {ctime()}.")
    print("")
    pprint(load_results())  # TODO
