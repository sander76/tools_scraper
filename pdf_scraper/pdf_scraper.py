import logging
from pathlib import PurePath, Path
from urllib.parse import urljoin

import requests

from pdf_scraper.helpers import traverse_server_folders, make_filename, \
    get_site_part

lgr = logging.getLogger(__name__)


def create_folder(folder: PurePath):
    _pth = Path(folder)
    if _pth.exists():
        pass
    else:
        lgr.debug("Path does exist: {}".format(_pth))
        _pth.mkdir(parents=True)


class PdfSource:
    def __init__(self, pdf_filename, output_path: PurePath, url, pdf_server):
        """
        :param pdf_filename: pdf filename.
        :param output_path: where to save the pdf file.
        :param url: URL to be converted to pdf
        :param pdf_server: server URL
        """
        self.output_filename = pdf_filename
        self.output_folder = output_path
        create_folder(output_path)
        self.pdf_server = '{}/url'.format(pdf_server)
        self.url = url
        self.output_full = PurePath(output_path,
                                    pdf_filename)

    def _get_pdf(self, url):
        """Makes a request to the pdf creation server. Returns a response
        with pdf data in the body."""
        # addr = '{}/url'.format(self.pdf_server)
        url = {'url': url}
        r = requests.get(self.pdf_server, params=url, stream=True, timeout=30)
        assert r.status_code == 200
        return r

    def create_pdf(self):
        """Create a pdf from the provided data."""
        try:
            r = self._get_pdf(self.url)
        except Exception as err:
            lgr.error("unable to create pdf from: {}".format(self.url))
            lgr.exception(err)
        else:
            with open(self.output_full, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)


class Scraper:
    def __init__(self,
                 site_base_folder,
                 site_base_url,
                 pdf_server):
        """
        :param site_base_folder: The root folder to be traversed for pdf conversion.
        :param site_base_url: The base url to be combined with the site folders.
        :param pdf_server: The server to convert the html to pdf.
        """
        self.site_folder = site_base_folder
        self.site = site_base_url
        self.pdf_server = pdf_server
        self.locations = []

    def scrape(self):
        lgr.debug("traversing base folder: {}".format(self.site_folder))
        self.locations = traverse_server_folders(self.site_folder)
        for _location in self.locations:
            _fname = make_filename(_location)
            _url = self.make_url(_location)
            lgr.debug(
                "making pdf from: location: {} filename: {} url: {}".format(
                    _location, _fname, _url))
            self._make_pdf(_fname, _location, _url, self.pdf_server)

    def _make_pdf(self, _filename, location, url, server):
        # temporarily replacing the filename with a generic one.

        pdf_source = PdfSource('document.pdf', location, url, server)
        pdf_source.create_pdf()

    def make_url(self, full_path: PurePath):
        """Make a url from a full path."""
        _path = get_site_part(full_path, self.site_folder)
        url = urljoin(self.site, '/'.join(_path.parts))
        return url + '/index.html'
