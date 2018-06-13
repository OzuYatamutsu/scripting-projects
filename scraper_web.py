from pickle import load
from time import ctime
from pprint import pprint
from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def render_results():
    return render_template(hotel_results=load_results())


def load_results(file='scraper_results.store') -> dict:
    with open(file, 'rb') as f:
        return load(f)

if __name__ == '__main__':
    app.run()
    #pprint(f"Last updated: {ctime()}.")
    #print("")
    #pprint(load_results())  # TODO
