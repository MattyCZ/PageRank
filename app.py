from flask import Flask, render_template, request

from forms import SearchForm
from search import Searcher

app = Flask(__name__)


@app.route('/')
def index():
    form = SearchForm()
    return render_template('main_page.html', form=form)


@app.route('/search_results')
def search_results():
    search_value = request.args['searchVal']
    vals = [{'name': 'Test', 'url': 'https://www.wikipedia.com', 'text': 'Toto je demonstrativní text'},
            {'name': 'TestTestovič', 'url': 'https://www.wikipedia.cz', 'text': 'Lorem ipsum dolor et samet'}]
    # s = Searcher()
    # vals = s.search(search_value)
    form = SearchForm()
    return render_template('search_results.html', search_value=search_value, return_values=vals, form=form)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
