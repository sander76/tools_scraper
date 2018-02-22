from pathlib import PurePath

from pdf_scraper.pdf_scraper import PdfSource


def test_pdfsource_init():
    pdf_source = PdfSource('test.pdf', PurePath('traverse_test'),
                           'https://127.0.0.1', 'http://pdfserver')
    assert pdf_source.output_full == PurePath('traverse_test/test.pdf')
