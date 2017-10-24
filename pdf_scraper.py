import os
import io

import time
import logging
import argparse
import requests
import make_booklet

from urllib.parse import urljoin
from lxml.html import parse
from logger.mylogger import setup_logging
from urllib.request import urlopen

def create_folder(folder):
    if os.path.exists(folder):
        pass
    else:
        os.makedirs(folder)


class PdfSource:
    def __init__(self, output_filename, output_path, url):
        self.output_filename = output_filename
        self.output_folder = output_path
        create_folder(output_path)
        self.url = url
        if "datasheet" in self.output_filename or "data sheet" in self.output_filename:
            self.datasheet = True
        else:
            self.datasheet = False
        self.output_full = os.path.join(output_path, output_filename)


def make_filename(link_text: str):
    return link_text.lstrip('_ ') + ".pdf"


class Scraper:
    def __init__(self, site, pdf_server, output_folder, css_selector=".dropdown-menu a"):
        self.site = site
        self.pdf_server = pdf_server
        self.output_folder = output_folder
        self.css_selector = css_selector
        self.parse_list = []
        # self.scrape()

    def scrape(self):
        dom = parse(urlopen(self.site)).getroot()
        links = dom.cssselect(self.css_selector)
        for link in links:
            fname = make_filename(link.text)
            try:
                self.parse_list.append(
                    PdfSource(fname, self.parse_filename(link.attrib['href']), self.parse_url(link.attrib['href'])))
            except UserWarning:
                pass

    def create_pdfs(self):
        for itm in self.parse_list:
            # time.sleep(5)
            if itm.datasheet:
                self.create_booklet(itm.url, itm.output_full)
            else:
                self.create_pdf(itm.url, itm.output_full)

    def _get_pdf(self, url):
        addr = '{}/url'.format(self.pdf_server)
        url = {'url': url}
        r = requests.get(addr, params=url, stream=True)
        assert r.status_code == 200
        return r

    def create_pdf(self, url, output):
        try:
            r = self._get_pdf(url)
        except AssertionError as e:
            lgr.error("unable to create pdf from: {}".format(url))
        else:
            with open(output, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)

    def create_booklet(self, url, output):
        try:
            r = self._get_pdf(url)
        except AssertionError as e:
            lgr.error("unable to create pdf from: {}".format(url))
        else:
            img_io = io.BytesIO()  # 3.5
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    img_io.write(chunk)
            img_io.seek(0)
            make_booklet.make_booklet(img_io, output)

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
