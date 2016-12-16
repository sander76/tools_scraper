import argparse
import logging

from logger.mylogger import setup_logging
from pdf_scraper import Scraper

parser = argparse.ArgumentParser()
parser.add_argument("site", help="the site to scrape")
parser.add_argument("pdf_server")
parser.add_argument("output_folder", help="output base folder for generated pdfs")


if __name__ == "__main__":
    setup_logging("logger/log_config.json")
    lgr = logging.getLogger(__name__)

    args = parser.parse_args()
    lgr.error("Starting the log.")
    for lp in range(10):
        scr = Scraper(args.site, args.pdf_server, args.output_folder)
        scr.scrape()
        scr.create_pdfs()
