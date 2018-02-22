import argparse
import logging

from pdf_scraper.helpers import ScraperError
from pdf_scraper.logger.mylogger import setup_logging
from pdf_scraper.pdf_scraper import Scraper

LOGGER=logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("site_base_folder",
                    help="output base folder for generated pdfs")
parser.add_argument("site_base_url", help="the site to scrape")
parser.add_argument("pdf_server")

if __name__ == "__main__":
    setup_logging("logger/log_config.json")
    lgr = logging.getLogger(__name__)

    args = parser.parse_args()
    lgr.error("Starting the log.")

    scr = Scraper(args.site_base_folder, args.site_base_url, args.pdf_server)
    try:
        scr.scrape()
    except ScraperError as err:
        LOGGER.error(err)
