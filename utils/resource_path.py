import os
import sys


def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and for PyInstaller.

    :param str relative_path: a relative path to the resource
    :return str: an absolute path to the resource
    """
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, relative_path)
