import os
from weasyprint import HTML
import logging

lgr = logging.getLogger(__name__)

def make_pdf(url,filename,file_save_location):
    filepath = os.path.join(file_save_location,filename)
    logging.debug("creating a pdf from: {}".format(url))
    logging.debug("saving it to       : {}".format(filepath))
    html = HTML(url)
    try:
        html.write_pdf(filepath)
    except MemoryError as e:
        lgr.error("Unable to create pdf from: {}".format(url))
    except Exception as e:
        lgr.error("Unable to create pdf from: {}".format(url))
        lgr.error(e)



