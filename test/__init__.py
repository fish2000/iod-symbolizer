# -*- coding: utf-8 -*-
from __future__ import print_function

symbolizer = None
symbolzer_imported = False

def import_module_at_path(pth, name=None):
    global symbolizer
    import os
    if not name:
        name = os.path.basename(pth)
    if os.path.isdir(pth):
        import sys
        sys.path.insert(0, pth)
        import importlib
        symbolizer = importlib.import_module(name)

def get_parent_directory():
    import os
    return os.path.dirname(os.path.dirname(__file__))

parent_directory = get_parent_directory()

def get_directory_in_project(name):
    global parent_directory
    import os
    target_directory = os.path.join(parent_directory, name)
    if os.path.isdir(target_directory):
        return target_directory
    return None

def import_project_directory(name):
    target_directory = get_directory_in_project(name)
    if target_directory:
        import_module_at_path(target_directory)
        return True
    return False

def import_local_symbolizer():
    import_project_directory('symbolizer')
    return symbolizer

# import symbolizer
if not import_local_symbolizer():
    raise ImportError("Local 'symbolizer' module not found!")
else:
    symbolizer_imported = True

__all__ = [import_local_symbolizer]
__all__ += symbolizer_imported and [symbolizer] or []

if __name__ == '__main__':
    print(dir(symbolizer))
    print(symbolizer.__file__)

