#!/usr/bin/env python
"""
Usage:
  symbolizer DIR [DIR ...] [-o OUTFILE] [-V | --verbose]
  symbolizer -h | --help | -v | --version
    
Options:
  -o OUTFILE --output=OUTFILE       specify output file [default: stdout]
  -V --verbose                      print verbose output
  -h --help                         show this text
  -v --version                      print version

"""

from __future__ import print_function
from os.path import join, isdir, dirname
from docopt import docopt
import parser as symbolizer
import sys

__version__ = "0.0.1"
exec(compile(open(join(dirname(dirname(__file__)), 'symbolizer-version.py')).read(),
             'symbolizer-version.py', 'exec'))

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
    directories = arguments.pop('DIR', [])
    if not directories:
        print("ERROR: Need to specify a directory to scan",
            file=sys.stderr)
        print(__doc__)
    
    # check directories
    for directory in directories:
        if not isdir(directory):
            print("ERROR: not a directory:",
                file=sys.stderr)
            print("\t%s" % directory,
                file=sys.stderr)
    
    # scan directories
    symbols = set()
    collected = set()
    for directory in directories:
        if verbose:
            print("> Scanning directory: %s" % directory,
                file=sys.stderr)
        collected |= symbolizer.collect(directory)
    
    # parse collected source files
    for source_file in sorted(collected):
        if verbose:
            print("> Parsing source: %s" % source_file,
                file=sys.stderr)
        symbols |= symbolizer.parse_source_file(source_file)
    
    # generate header
    if verbose:
        print("> Generating header:",
                file=sys.stderr)
    if output == "stdout":
        print()
        print(symbolizer.generate_header(symbols))
        print()
    else:
        if verbose:
            print("> Writing output: %s" % output,
                file=sys.stderr)
        with open(output, "wb") as fh:
            fh.write(symbolizer.geerate_header(symbols))
    
    # donezo.
    if verbose:
        print("> Done.")


if __name__ == '__main__':
    cli(sys.argv)