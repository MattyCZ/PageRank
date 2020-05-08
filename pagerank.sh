#!/bin/sh
file=graphScraper/sitegraph.json
if [ -f "$file" ]; then
  rm -r $file
fi
cd graphScraper
scrapy crawl graph_scraper
cd ..
python pageRank.py