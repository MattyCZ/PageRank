import os

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
# scraper.run(max_pages=100, start_urls=['https://en.wikipedia.org/wiki/Main_Page', 'https://dmoz-odp.org/'], stay_on_domains=False)

graph = Graph()
# graph.createNewGraph(scraped_data,graph_data)
graph.loadExisting(graph_data)

indexer = Indexer()
# indexer.createIndex(graph_data, indexdir)

pageRank = PageRank(graph)

searcher = Searcher(pageRank, indexer)


@app.route('/')
def index():
    form = SearchForm()
    return render_template('main_page.html', form=form)


@app.route('/search_results')
def search_results():
    search_value = request.args['searchVal']
    vals = searcher.search(indexdir, search_value)
    form = SearchForm()
    return render_template('search_results.html', search_value=search_value, return_values=vals, form=form)


@app.route('/scrape_new', methods=['GET', 'POST'])
def scrape_data():
    form = SearchForm()
    scrape_form = ScrapeForm()
    if request.method == 'POST':
        os.system(f'python scrapeScript.py {scrape_form.max_pages} "{scrape_form.start_url}" {scrape_form.stay_on_domain}')
        graph.createNewGraph(scraped_data, graph_data)
        indexer.createIndex(graph_data, indexdir)
    else:
        print(request.method)
    return render_template('scrape_new.html', form=form, scrape_form=scrape_form)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, threaded=False, processes=1)
