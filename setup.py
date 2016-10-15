#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.0.1"
exec(compile(open('symbolizer/version.py').read(),
             'symbolizer/version.py', 'exec'))

name = 'symbolizer'
long_name = 'iod-symbolizer'
version = __version__
packages = [name]
description = "Parse C/C++/Objective-C/Objective-C++ source for IOD symbols and output header files"

keywords = [
    'IOD','C','C++','Objective-C','Objective-C++','C++11','C++14',
    'Preprocessor','Parser','Symbols','Header'
]

long_description = """
    
    iod-symbolizer - Parse C/C++/Objective-C/Objective-C++ source for IOD symbols and output header files.
    
"""


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Other Environment',
    'Environment :: Plugins',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Topic :: Database',
    'Topic :: Utilities',
]

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys

if 'sdist' in sys.argv and 'upload' in sys.argv:
    """ CLEAN THIS MESS UP RIGHT NOW YOUNG MAN """
    import commands
    import os
    finder = "/usr/bin/find %s \( -name \*.pyc -or -name .DS_Store \) -delete"
    theplace = os.getcwd()
    if theplace not in (".", "/"):
        print("+ Deleting crapola from %s..." % theplace)
        print("$ %s" % finder % theplace)
        commands.getstatusoutput(finder % theplace)
        print("")

setup(

    name=long_name, version=version, description=description,
    long_description=long_description,
    download_url=('http://github.com/fish2000/%s/zipball/master' % long_name),

    author=u"Alexander Bohn",
    author_email='fish2000@gmail.com',
    url='http://github.com/fish2000/%s' % long_name,
    license='GPLv2',
    keywords=', '.join(keywords),
    platforms=['any'],
    
    include_package_data=True,
    zip_safe=False,
    
    packages=[]+packages,
    
    package_dir={
        'symbolizer': 'symbolizer',
    },
    
    entry_points={
        'console_scripts': [
            'symbolizer = symbolizer.cli:cli'
        ],
    },
    
    package_data={
        'symbolizer': [
            '*.cmake'
        ]},
    install_requires=['docopt', 'PyYAML'],

    classifiers=classifiers+[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy'],
)

