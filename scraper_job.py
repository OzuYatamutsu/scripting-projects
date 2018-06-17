from scraper import (
    is_hyatt_available, is_hilton_available, is_mariott_available,
    is_sharaton_available, is_westin_available, is_hotel_indigo_available
)
from pickle import dump
from os import rename, mkdir
from os.path import isdir
from time import time
OUTPUT_FILE = 'scraper_results.store'
OUTPUT_META_FILE = 'scraper_meta.store'
OUTPUT_SCREENSHOT = 'final_state.png'
OUTPUT_URL = '.url'


def sync(mock=False):
    CHECKS_TO_RUN = {
        'Hyatt': is_hyatt_available, 'Hilton': is_hilton_available, 'Mariott': is_mariott_available,
        'Sharaton': is_sharaton_available, 'Westin': is_westin_available, 'Hotel Indigo': is_hotel_indigo_available
    }

    sync_result = {}
    meta_result = {}

    if not isdir('screengrabs'):
        mkdir('screengrabs')

    for hotel, check_func in CHECKS_TO_RUN.items():
        try:
            print(f"Running {check_func.__name__}...")
            sync_result[hotel] = check_func() if not mock else (False, 'DEBUG')
            try:
                # filename = f"screengrabs/{check_func.__name__}_{str(int(time()))}.png"
                path = '/var/www/staging' 
                filename = f"{check_func.__name__}_{str(int(time()))}.png"

                rename(OUTPUT_SCREENSHOT, f'{path}/{filename}')
                with open(OUTPUT_URL, 'r') as f:
                    url = f.readline()

                meta_result[hotel] = {'url': url, 'screenshot': filename}
            except Exception as e:
                meta_result[hotel] = {'url': '', 'screenshot': str(e)}
        except Exception as e:
            sync_result[hotel] = (False, str(e))

    # Store results to file system
    with open(OUTPUT_FILE, 'wb') as f:
        dump(sync_result, f)
    with open(OUTPUT_META_FILE, 'wb') as f:
        dump(meta_result, f)


if __name__ == '__main__':
    sync()
