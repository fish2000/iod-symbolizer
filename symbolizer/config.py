
from __future__ import print_function

import yaml
from os.path import join, isdir, isfile, expanduser

def parse(configuration, check=True):
    config_dict = yaml.safe_load(configuration)
    if not check:
        return config_dict
    
    root = expanduser(config_dict['root'])
    assert isdir(root)
    for sourcedir in config_dict['source']:
        assert isdir(join(root, sourcedir))
    
    if 'suffixes' in config_dict:
        assert len(config_dict['suffixes']) > 0
    if 'reserved' in config_dict:
        assert len(config_dict['reserved']) > 0
    
    target = config_dict.get('target')
    if 'file' in target:
        targfile = join(root, target.get('file'))
        if not target.get('overwrite'):
            if isfile(targfile):
                raise IOError("File output target exists,\n"
                              "but configuration forbids overwriting\n")
    return config_dict

