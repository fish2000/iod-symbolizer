#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import unittest2 as unittest
import sample
from test import import_local_symbolizer
symbolizer = import_local_symbolizer()
u = symbolizer.symbolizer_unicode

MAX_DIFF = 2500

class SymbolizerTests(unittest.TestCase):
    
    def setUp(self):
        self.maxDiff = MAX_DIFF
    
    def test_symbolize(self):
        source_edit = (sample.input,)
        for blockout_re in (symbolizer.quotes, symbolizer.dbl_quotes,
                            symbolizer.cpp_comments, symbolizer.c_comments):
            source_edit = blockout_re.subn(symbolizer.blockout, source_edit[0])
        try:
            sym = set(symbolizer.symbol_re.findall(source_edit[0])) - symbolizer.KEYWORDS
        except:
            sym = set()
        
        self.assertEqual(sym, sample.output)
    
    def test_symbolize_parse(self):
        self.assertEqual(symbolizer.parse(sample.input), sample.output)
    
    def test_generate_header(self):
        header = symbolizer.generate_header(sorted(sample.output), when="RIGHT NOW")
        self.assertMultiLineEqual(header, sample.header)


class ParserObjectTests(unittest.TestCase):
    
    def setUp(self):
        from os.path import split, expanduser
        self.tmps = []
        self.userpath = expanduser('~')
        self.user = split(self.userpath)[1]
        self.parser = symbolizer.Parser(**sample.arguments)
        self.maxDiff = MAX_DIFF
    
    def tearDown(self):
        from os import remove
        for tmp in self.tmps:
            remove(tmp)
    
    def test_manual_symbolize(self):
        source_edit = (sample.input,)
        for blockout_re in (self.parser.quotes, self.parser.dbl_quotes,
                            self.parser.cpp_comments, self.parser.c_comments):
            source_edit = blockout_re.subn(self.parser.blockout, source_edit[0])
        try:
            sym = set(self.parser.symbol_re.findall(source_edit[0])) - self.parser.keywords
        except:
            sym = set()
        
        self.assertEqual(sym, sample.output)
    
    def test_parser_object_parse(self):
        self.parser.parse(sample.input)
        self.assertEqual(self.parser.symtab, sample.output)
    
    def test_parser_object_parse_file(self):
        tmp = self.parser.tmpwrite(sample.input)
        self.tmps.append(tmp)
        self.parser.parse_file(tmp)
        self.assertEqual(self.parser.symtab, sample.output)
    
    def test_generate_header(self):
        header = symbolizer.generate_header(sorted(sample.output), when="RIGHT NOW")
        self.assertMultiLineEqual(header, sample.header)
    
    def test_parser_object_property_root(self):
        from os.path import expanduser
        self.assertEqual(self.parser.root, expanduser(sample.arguments['--root']))
    
    def test_parser_object_property_suffixes(self):
        self.assertEqual(self.parser.suffixes, symbolizer.SUFFIXES)
    
    def test_parser_object_property_directories(self):
        from os.path import join
        self.assertEqual(self.parser.directories, (
            join(self.userpath, 'Dropbox/libimread/src'),
            join(self.userpath, 'Dropbox/libimread/include/libimread'),
        ))


from symbolizer import config
from os.path import join, isdir, expanduser

class ConfigTests(unittest.TestCase):
    
    def setUp(self):
        self.maxDiff = MAX_DIFF
    
    def test_parse_config(self):
        config_dict = config.parse(sample.config)
        
        root = expanduser(config_dict['root'])
        
        self.assertTrue(isdir(root))
        for sourcedir in config_dict['source']:
            self.assertTrue(isdir(join(root, sourcedir)))
        
        if 'suffixes' in config_dict:
            self.assertNotEqual(len(config_dict['suffixes']), 0)
        if 'reserved' in config_dict:
            self.assertNotEqual(len(config_dict['reserved']), 0)


VERBOSITY = 2

# testload = lambda testmod: unittest.TestLoader().loadTestsFromTestCase(testmod)
# testsuite = lambda suites: unittest.TestSuite([testload(suite) for suite in suites])
# testrun = lambda *suites: unittest.TextTestRunner(verbosity=VERBOSITY).run(testsuite(suites))

# if __name__ == '__main__':
#     testrun(
#         SymbolizerTests,
#         ParserObjectTests,
#         ConfigTests)

if __name__ == '__main__':
    pass