import os
from urllib.parse import urljoin
from lxml.html import parse
import logging
import argparse
import requests
from logger.mylogger import setup_logging


class PdfSource:
    def __init__(self, output_filename, output_path, url):
        self.output_filename = output_filename
        self.output_folder = output_path
        self.url = url
        self.output_full = os.path.join(output_path, output_filename)


class Scraper:
    def __init__(self, site, pdf_server, output_folder):
        self.site = site
        self.pdf_server = pdf_server
        self.output_folder = output_folder
        self.parse_list = []
        #self.scrape()



    def scrape(self):
        dom = parse(self.site).getroot()
        links = dom.cssselect('.dropdown-menu a')
        for link in links:
            fname = link.text + ".pdf"
            try:
                self.parse_list.append(
                    PdfSource(fname, self.parse_filename(link.attrib['href']), self.parse_url(link.attrib['href'])))
            except UserWarning:
                pass

    def create_pdfs(self):
        for itm in self.parse_list:
            self.create_pdf(itm.url, itm.output_full)

    def create_pdf(self, url, output):
        addr = '{}/url'.format(self.pdf_server)
        url = {'url': url}
        r = requests.get(addr,params=url, stream=True)
        with open(output, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    def parse_url(self, url):
        url = urljoin(self.site, url)
        return url + 'index.html'

    def parse_filename(self, url):
        try:
            parts = url.split('/')
            # doing a check if there is a filename present. Dirty hack.
            fname = parts[-2] + ".pdf"
            folders = self.create_ftp_path(parts)
        except IndexError as e:
            raise UserWarning('skip this one')
        else:
            return folders

    def create_ftp_path(self, folderlist):
        return os.path.join(self.output_folder, *folderlist)


parser = argparse.ArgumentParser()
parser.add_argument("site", help="the site to scrape")
parser.add_argument("pdf_server")
parser.add_argument("output_folder", help="output base folder for generated pdfs")

if __name__ == "__main__":
    setup_logging("logger/log_config.json")
    lgr = logging.getLogger(__name__)

    args = parser.parse_args()
    lgr.error("Starting the log.")

    scr = Scraper(args.site, args.pdf_server, args.output_folder)
    scr.scrape()
    scr.create_pdfs()

