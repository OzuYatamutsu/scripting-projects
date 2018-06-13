from pickle import load
from time import ctime
from pprint import pprint
from os import stat
from flask import Flask, render_template
app = Flask(__name__)
DEFAULT_STORE_FILE = 'scraper_results.store'



@app.route('/')
def render_results():
    return render_template(
        'status.html',
        hotel_results=load_results(),
        last_modified=f"{ctime(stat(DEFAULT_STORE_FILE).st_ctime)} (Eastern Time)"
    )


def load_results(file=DEFAULT_STORE_FILE) -> dict:
    with open(file, 'rb') as f:
        return load(f)

if __name__ == '__main__':
    app.run(port=42716)
