from pickle import load


def load_results(file='scraper_results.store') -> dict:
    with open(file, 'rb') as f:
        return load(f)

if __name__ == '__main__':
    print(str(load_results()))  # TODO