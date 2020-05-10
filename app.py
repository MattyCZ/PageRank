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
    # Potrebuju do promenne return_values v render template narvat neco takoveho. Vsechny ty veci jsou
    # pouzity v templatu, takze funkce co bude hledat v databazi bude muset vracet nejakou formu listu
    # slovniku, ktery v sobe maji name, url a text(to bude asi prvnich x pismen, nahled). Pokud by se
    # to melo jmenovat jinak tak to v templatu klidne zmen. Slovo mas v promenne search value
    search_value = request.args['searchVal']
    s =  Searcher()
    vals = s.search(search_value) 
    tmp_values = [{'name': 'Test', 'url': 'https://www.wikipedia.com', 'text': 'Toto je demonstrativní text'},
                  {'name': 'TestTestovič', 'url': 'https://www.wikipedia.cz', 'text': 'Lorem ipsum dolor et samet'}]
    return render_template('search_results.html', search_value=search_value, return_values=vals)


if __name__ == '__main__':
    app.run(debug=True)
