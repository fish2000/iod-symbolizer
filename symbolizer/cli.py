#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import parser as symbolizer

__doc__ = """
Usage:
  symbolizer (-c CONFIG.yml | DIR [DIR ...]
                 [-r ROOTDIR] [-o OUTPUT]
    [--numeric] [--mixedcase] [--uppercase]
                    [-S suf,fix,es,etc ...]
                    [-R r,r0,r1,r2,etc ...])
             [-V | --verbose]
  symbolizer  -h | --help
  symbolizer  -v | --version
    
Options:
  -c CONFIG.yml --config=CONFIG.yml    read options from CONFIG.yml (overrides CLI)
  -r ROOTDIR --root=ROOTDIR            root dir for resolving paths [default: CWD]
  -o OUTPUT --output=OUTPUT            output file [default: stdout]
  --numeric                            symbolize 8754 (numeric) tokens [default: false]
  --mixedcase                          symbolize Mixed_Case_Tokens [default: false]
  --uppercase                          symbolize UPPER_CASE_TOKENS [default: false]
  -S suf,fix,es --suffixes=suf,fix,es  file suffixes to parse [default: %s]
  -R r,r0,r1,r2 --reserved=r,r0,r1,r2  extra reserved words (DON'T symbolize these)
  -V --verbose                         print verbose output
  -h --help                            show this text
  -v --version                         print version

""" % ", ".join(tuple(symbolizer.SUFFIXES))

from os.path import join, isdir, dirname
from docopt import docopt
import templates
import sys

__version__ = "0.0.1"
exec(compile(open(join(dirname(__file__), 'version.py')).read(),
             'version.py', 'exec'))

def err(text="", **kwargs):
    print(text, file=sys.stderr)

def noop(*args, **kwargs):
    pass

def cli(argv=None):
    if not argv:
        argv = sys.argv
    
    arguments = docopt(__doc__, argv=argv[1:],
                                help=True,
                                version=__version__)
    
    # print(argv)
    # print(arguments)
    # sys.exit()
    
    verbose = arguments.pop('--verbose', False)
    output = arguments.pop('--output')
    pp = verbose and err or noop
    
    directories = arguments.pop('DIR', [])
    if not directories:
        err("ERROR: Need to specify a directory to scan")
        err(__doc__)
    
    # check directories
    for directory in directories:
        if not isdir(directory):
            err("ERROR: not a directory:")
            err("\t%s" % directory)
    
    # scan directories
    symbols = set()
    collected = set()
    for directory in directories:
        pp("> Scanning directory: %s" % directory)
        collected |= symbolizer.collect(directory)
    
    # parse collected source files
    for source_file in sorted(collected):
        pp("> Parsing source: %s" % source_file)
        symbols |= symbolizer.parse_source_file(source_file)
    
    # generate header
    pp("> Generating header:")
    header = templates.generate_header(symbols)
    if output == "stdout":
        print()
        print(header)
        print()
    else:
        pp("> Writing output: %s" % output)
        with open(output, "wb") as fh:
            fh.write(header)
    
    # donezo.
    pp("> Done.")


if __name__ == '__main__':
    cli(sys.argv)