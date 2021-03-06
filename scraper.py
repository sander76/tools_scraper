import os
from urllib.parse import urljoin
from lxml.html import parse
import logging
import argparse
from shutil import rmtree

from logger.mylogger import setup_logging


def create_ftp_path(base_ftp_path, folderlist):
    return os.path.join(base_ftp_path, *folderlist)


def parse_filename(base_path, url):
    try:
        parts = url.split('/')
        # doing a check if there is a filename present. Dirty hack.
        fname = parts[-2] + ".pdf"
        folders = create_ftp_path(base_path, parts)
    except IndexError as e:
        raise UserWarning('skip this one')
    else:
        return folders


def parse_url(base_url, url):
    url = urljoin(base_url, url)
    return url + 'index.html'


def create_folder(folder):
    if os.path.exists(folder):
        pass
    else:
        os.makedirs(folder)


def clear_base_folder(base_folder):
    try:
        rmtree(base_folder)
    except FileNotFoundError:
        pass


parser = argparse.ArgumentParser()
parser.add_argument("site", help="the site to scrape")
parser.add_argument("build_folder", help="output base folder for generated pdfs")

if __name__ == "__main__":
    setup_logging("logger/log_config.json")
    lgr = logging.getLogger(__name__)

    args = parser.parse_args()
    from create_pdf import make_pdf
    lgr.error("Starting the log.")
    clear_base_folder(args.build_folder)
    dom = parse(args.site).getroot()
    links = dom.cssselect('.dropdown-menu a')
    parselist = []
    for link in links:
        fname = link.text + ".pdf"
        try:
            parselist.append(
                # (parse_url(args.site, link.attrib['href']), *parse_filename(args.build_folder, link.attrib['href'])))
                (parse_url(args.site, link.attrib['href']),
                 fname,
                 parse_filename(args.build_folder, link.attrib['href'])))
        except UserWarning:
            pass

    for prs in parselist:
        create_folder(prs[2])
        logging.debug("{} - {} - {}".format(prs[0], prs[1], prs[2]))
        make_pdf(prs[0], prs[1], prs[2])
