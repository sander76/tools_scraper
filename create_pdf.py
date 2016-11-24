import os
from weasyprint import HTML

def make_pdf(url,filename,file_save_location):
    filepath = os.path.join(file_save_location,filename)
    html = HTML(url)
    html.write_pdf(filepath)