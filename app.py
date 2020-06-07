import os
import subprocess
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from forms import SearchForm, ScrapeForm
from scraper import Scraper
from graph import Graph
from indexer import Indexer
from pageRank import PageRank
from searcher import Searcher

app = Flask(__name__)
Bootstrap(app)

scraped_data = f'{os.path.dirname(os.path.realpath(__file__))}/scraped_data.json'
graph_data = f'{os.path.dirname(os.path.realpath(__file__))}/graph_data.json'

indexdir = 'indexdir'

scraper = Scraper(scraped_data)
graph = Graph()
indexer = Indexer()


@app.route('/')
def index():
    """
    Displays main page.
    """
    form = SearchForm()
    return render_template('main_page.html', form=form)


@app.route('/search_results')
def search_results():
    """
    Displays search results ordered by pagerank.
    """
    graph.loadExisting(graph_data)
    pageRank = PageRank(graph)
    searcher = Searcher(pageRank, indexer)
    search_value = request.args['searchVal']
    vals = searcher.search(indexdir, search_value)
    form = SearchForm()
    return render_template('search_results.html', search_value=search_value, return_values=vals, form=form)


@app.route('/scrape_new', methods=['GET', 'POST'])
def scrape_new():
    """
    Allows to modify scraping source or amount of scraped data. New data can overwrite
    old or can be appended
    """
    form = SearchForm()
    scrape_form = ScrapeForm()
    if request.method == 'POST':
        max_pages = str(request.form['max_pages'])
        start_url = str(request.form['start_url'])
        stay_on_domain = str(request.form['stay_on_domain'])
        update_existing = request.form['update_existing']

        # Scraping needs to be called from main thread
        subprocess.call(['python', 'scrapeScript.py', scraped_data, max_pages, start_url, stay_on_domain])
        if update_existing == 'True':
            graph.addToExisting(graph_data, scraped_data, graph_data)
            indexer.updateIndex(graph_data, indexdir)
        else:
            graph.createNewGraph(scraped_data, graph_data)
            indexer.createIndex(graph_data, indexdir)
    else:
        print(request.method)
    return render_template('scrape_new.html', form=form, scrape_form=scrape_form)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, threaded=False, processes=1)
