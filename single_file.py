import argparse
import json
import logging
from pdf_scraper import Scraper
lgr=logging.getLogger(__name__)
parser = argparse.ArgumentParser()
parser.add_argument("jsfile", help="the site to scrape")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    args = parser.parse_args()
    config_file = args.jsfile
    with open(config_file) as fl:
        _js=json.load(fl)
    lgr.debug(_js['site'])
    lgr.debug(_js['pdf_scraper'])
    lgr.debug(_js['output'])

    pdfer = Scraper('', _js['pdf_scraper'], _js['output'])
    pdfer.create_pdf(_js['site'], _js['output'] + '/test.pdf')
