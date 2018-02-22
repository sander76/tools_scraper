from pathlib import PurePath
from unittest.mock import Mock, call

import pytest

from pdf_scraper.pdf_scraper import Scraper

SITE_FOLDER = 'traverse_test'
PDF_SERVER = 'https://100.0.0.0:5612'
WEB_BASE_URL = 'https://192.168.2.9'


@pytest.fixture
def fake_scraper():
    return Scraper(SITE_FOLDER,
                   WEB_BASE_URL,
                   PDF_SERVER)


def test_make_url(fake_scraper):
    _url = '/api/test'
    val = fake_scraper.make_url(PurePath(SITE_FOLDER + _url))
    assert val == WEB_BASE_URL + _url + '/index.html'
    assert val == 'https://192.168.2.9/api/test/index.html'

def test_wrong_formed_url(fake_scraper):
    _url = '/api/test'
    fake_scraper.site ='htp://test'
    val = fake_scraper.make_url(PurePath(SITE_FOLDER +_url))


def test_make_pdf(fake_scraper):
    mock = Mock()

    fake_scraper._make_pdf = mock
    fake_scraper.scrape()
    calls = [call('traverse_test.pdf', PurePath('traverse_test'),
                  'https://192.168.2.9/index.html', 'https://100.0.0.0:5612'),
             call('level_2_1.pdf',
                  PurePath('traverse_test/level1_1/level_2_1'),
                  'https://192.168.2.9/level1_1/level_2_1/index.html',
                  'https://100.0.0.0:5612'),
             call('level1_3.pdf', PurePath('traverse_test/level1_3'),
                  'https://192.168.2.9/level1_3/index.html',
                  'https://100.0.0.0:5612')]
    mock.assert_has_calls(calls)
    #assert mock.assert_called_with('fl', 'fl', 'fl')
