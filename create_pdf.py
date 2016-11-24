import os
from weasyprint import HTML
import logging

def make_pdf(url,filename,file_save_location):
    filepath = os.path.join(file_save_location,filename)
    logging.debug("creating a pdf from: {}".format(url))
    logging.debug("saving it to       : {}".format(filepath))
    html = HTML(url)
    html.write_pdf(filepath)

