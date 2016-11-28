import argparse

from pdf_scraper import Scraper

parser = argparse.ArgumentParser()
parser.add_argument("page", help="the site to scrape")
parser.add_argument("pdf_server")
parser.add_argument("output_folder", help="output base folder for generated pdfs")

if __name__=="__main__":
    args = parser.parse_args()
    pdfer = Scraper('',args.pdf_server,args.output_folder)
    pdfer.create_pdf(args.page,args.output_folder+'/test.pdf')