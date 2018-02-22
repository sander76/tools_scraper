import os
from pathlib import PurePath


class ScraperError(Exception):
    pass


def traverse_server_folders(base_folder) -> [PurePath]:
    if os.path.exists(base_folder):
        folders = []

        def traverse(_folder):
            for dirpath, dirnames, filenames in os.walk(_folder):
                if 'index.html' in filenames:
                    folders.append(PurePath(dirpath))
                # for _dirname in dirnames:
                #     traverse(os.path.join(dirpath, _dirname))

        traverse(base_folder)
        return folders
    else:
        raise ScraperError("folder does not exist {}".format(base_folder))


def make_filename(link_text: PurePath):
    _fname = link_text.name
    return _fname.lstrip('_ ') + ".pdf"


def get_site_part(full_path: PurePath, root_site_folder: str) -> PurePath:
    """Gets the folder path relative to the output site folder.

    The full_path may be a full resource path. We need the path relative
    to the site_folder name to make a usefull url in the end."""
    _full_path = PurePath(full_path)

    new_path = _full_path.relative_to(root_site_folder)
    return new_path
    #
    # _parts = _full_path.parts
    # _new_path = None
    # for idx, _part in enumerate(_parts):
    #     if _part == site_folder:
    #         _new_path = PurePath(*_parts[idx + 1:])
    #         break
    # if _new_path:
    #     # todo: check whether the site_folder is still in the path meaning it is a duplicate name and as a result should raise a fatal error.
    #     return _new_path
    # return _full_path
