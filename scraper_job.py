from scraper import (
    is_hyatt_available, is_hilton_available, is_mariott_available,
    is_sharaton_available, is_westin_available
)
from pickle import dump
OUTPUT_FILE = 'scraper_results.store'


def sync(mock=False):
    CHECKS_TO_RUN = {
        'Hyatt': is_hyatt_available, 'Hilton': is_hilton_available, 'Mariott': is_mariott_available,
        'Sharaton': is_sharaton_available, 'Westin': is_westin_available
    }

    sync_result = {}

    for hotel, check_func in CHECKS_TO_RUN.items():
        try:
            print(f"Running {check_func.__name__}...")
            sync_result[hotel] = check_func() if not mock else (False, 'DEBUG')
        except Exception as e:
            sync_result[hotel] = (False, str(e))

    # Store results to file system
    with open(OUTPUT_FILE, 'wb') as f:
        dump(sync_result, f)


if __name__ == '__main__':
    sync()
