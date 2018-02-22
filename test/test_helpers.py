from pathlib import PurePath

from pdf_scraper.helpers import traverse_server_folders, make_filename, \
    get_site_part


def test_traverse_folder():
    base_path = 'traverse_test'
    folders = traverse_server_folders(base_path)
    assert len(folders) == 3
    assert PurePath('traverse_test') in folders

    assert PurePath('traverse_test/level1_1/level_2_1') == folders[1]

    assert PurePath('traverse_test/level1_3') == folders[2]

    _path = folders[1]
    assert 'level_2_1' == _path.name


def test_make_file_name():
    _path = PurePath('traverse_test/level1_1/level_2_1')
    assert make_filename(_path) == 'level_2_1.pdf'

    _path = PurePath('traverse_test')
    assert make_filename(_path) == 'traverse_test.pdf'

    _path = PurePath('traverse_test/_level1')
    assert make_filename(_path) == 'level1.pdf'

    _path = PurePath('traverse_test/ level1')
    assert make_filename(_path) == 'level1.pdf'

    _path = PurePath('traverse_test/ _level1')
    assert make_filename(_path) == 'level1.pdf'


def test_get_site_part():
    full = PurePath('c:/abc/site/traverse_test/level1')
    base_path = 'c:/abc/site/'
    _path = get_site_part(full, base_path)
    assert _path == PurePath('traverse_test/level1')

    # full = '/abc/site1/traverse_test/level1'
    # _path = get_site_part(full, 'site1')
    # assert _path == PurePath('traverse_test/level1')
    #
    # full = 'traverse_test/level1'
    # _path = get_site_part(full)
    # assert _path == PurePath('traverse_test/level1')
