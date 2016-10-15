#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import re
import sys
import functools
from itertools import ifilter, imap
from os.path import join, expanduser, abspath, isdir
from os import walk, getcwd

SUFFIXES = set((
    r"c",
    r"cc", r"cpp", r"cxx", r"c\+\+",
    r"m",
    r"mm", r"mpp", r"mxx", r"m\+\+",
    r"h",
    r"hh", r"hpp", r"hxx", r"h\+\+",
    r"inl"
))

KEYWORDS = set((
    "alignas", "alignof", "and", "and_eq", "assert", "asm", "auto",
    "bitand", "bitor", "bool", "break",
    "case", "catch", "char", "char16_t", "char32_t", "class",
    "compl", "const", "constexpr", "const_cast", "continue",
    "decltype", "default", "delete", "do", "double", "dynamic_cast",
    "else", "enum", "explicit", "export", "extern",
    "false", "float", "for", "friend",
    "goto",
    "if", "inline", "int",
    "long",
    "mutable",
    "namespace", "new", "noexcept", "not", "not_eq", "nullptr",
    "operator", "or", "or_eq",
    "private", "protected", "public",
    "register", "reinterpret_cast", "return",
    "short", "signed", "sizeof", "static", "static_assert",
    "static_cast", "struct", "switch",
    "template", "this", "thread_local", "throw", "true",
    "try", "typedef", "typeid", "typename",
    "union", "unsigned", "using",
    "virtual", "void", "volatile",
    "wchar_t", "while",
    "xor", "xor_eq"))

SYMBOL_PREFIX = r'_'

sanitizer = re.compile(r'\W+')
symbol_re = re.compile(r"(?:\W+|^)(?:%s)([0-9a-z][0-9a-z_]+)(?!_t)" % SYMBOL_PREFIX)
suffix_re = re.compile(r"(%s)$" % ("|".join(map(
    lambda suffix: r"\.%s" % suffix, SUFFIXES))))

quotes          = re.compile(r"'(.*)'",     re.MULTILINE)
dbl_quotes      = re.compile(r'"(.*)"',     re.MULTILINE)
cpp_comments    = re.compile(r'//(.*)\n',   re.MULTILINE)
c_comments      = re.compile(r'/\*(.*)\*/', re.MULTILINE)
blockout        = lambda match: "#" * len(match.group(0))

def collect_files(root_dir, suffixes):
    """ Collect files recursively that match one or more file suffixes.
    """
    collected = set()
    suffix_re = re.compile(r"(%s)$" % ("|".join(map(
        lambda suffix: r"\.%s" % suffix, suffixes))))
    
    for pth, dirs, files in walk(expanduser(root_dir)):
        found = set(imap(lambda file: join(pth, file),
            ifilter(lambda file: suffix_re.search(file, re.IGNORECASE), files)))
        collected |= found
    return collected

def sanitize_suffixes(*suffixes):
    """ Ensure suffixes (which may be passed in from the user) are clean
    """
    return set((suffix.lower() for suffix in suffixes))

collect = functools.partial(collect_files, suffixes=list(sanitize_suffixes(*SUFFIXES)))

def parse(source):
    source_edit = (source,)
    for blockout_re in (quotes, dbl_quotes, cpp_comments, c_comments):
        source_edit = blockout_re.subn(blockout, source_edit[0])
    try:
        sym = set(symbol_re.findall(source_edit[0]))
    except:
        return set()
    return sym - KEYWORDS

def parse_source_file(file_name):
    with open(file_name, "rb") as fh:
        source_file = fh.read()
    return parse(source_file)

def err(_, text="", **kwargs):
    print(text, file=sys.stderr)

def noop(_, *args, **kwargs):
    pass

class ParserArgumentError(ValueError):
    pass

class Parser(object):
    
    quotes          = re.compile(r"'(.*)'",     re.MULTILINE)
    dbl_quotes      = re.compile(r'"(.*)"',     re.MULTILINE)
    cpp_comments    = re.compile(r'//(.*)\n',   re.MULTILINE)
    c_comments      = re.compile(r'/\*(.*)\*/', re.MULTILINE)
    blockout        = lambda cls, match: "#" * len(match.group(0))
    
    @staticmethod
    def read(file_name):
        from os.path import expanduser, isfile
        file_name = expanduser(file_name)
        if not isfile(file_name):
            raise IOError("nothing to read from path: %s" % file_name)
        with open(file_name, "rb") as fh:
            contents = fh.read()
        return contents
    
    @staticmethod
    def write(file_name, with_what="", overwrite=True):
        from os.path import expanduser, isfile
        file_name = expanduser(file_name)
        if not overwrite and isfile(file_name):
            raise IOError("won't overwrite to path: %s" % file_name)
        if not with_what:
            raise IOError("nothing to write to path: %s" % file_name)
        with open(file_name, "wb") as fh:
            fh.write(with_what)
    
    @classmethod
    def tmpwrite(cls, with_what="", suffix=".tmp"):
        import tempfile
        tf = tempfile.mktemp(suffix=suffix)
        cls.write(tf, with_what=with_what, overwrite=False)
        return tf
    
    @classmethod
    def err(cls, message=None):
        if not message:
            message = "error in parser arguments"
        return ParserArgumentError(message)
    
    def __init__(self, *args, **arguments):
        super(Parser, self).__init__()
        
        self.keywords = KEYWORDS
        self.suffixes = SUFFIXES
        self.collected = set()
        self.symbols = set()
        
        self.verbose = arguments.pop('--verbose', False)
        self.pp = self.verbose and err or noop
        
        symbolize_opts = dict(
            prefix=arguments.pop('--prefix', SYMBOL_PREFIX),
            numeric=arguments.pop('--numeric', False),
            mixedcase=arguments.pop('--mixedcase', False),
            uppercase=arguments.pop('--uppercase', False))
        
        symbol_init_range = r'a-z'
        symbol_main_range = r'0-9a-z_'
        
        # THIS IS SOME HACK SHIT
        if symbolize_opts['numeric']:
            symbol_init_range = r'0-9' + symbol_init_range
        if symbolize_opts['mixedcase'] or symbolize_opts['uppercase']:
            symbol_main_range = r'0-9a-zA-Z_'
            if symbolize_opts['uppercase']:
                # for now 'mixed-case' is implied
                symbol_init_range = symbol_init_range + r'A-Z'
        
        self.symbol_re = re.compile(
            r"(?:\W+|^)(?:%s)([%s][%s]+)(?!_t)" % (
                symbolize_opts['prefix'],
                symbol_init_range,
                symbol_main_range))
        
        self.keywords |= set(arguments.pop('--reserved', []))
        self.suffixes |= set(arguments.pop('--suffixes', []))
        self.suffix_re = re.compile(r"(%s)$" % ("|".join(map(
            lambda suffix: r"\.%s" % suffix, list(self.suffixes)))))
        
        self.root = arguments.pop('--root', "CWD")
        self.directories = arguments.pop('DIR', [])
    
    def collect(self, collect_root):
        self.pp("> Scanning directory: %s" % collect_root)
        for pth, dirs, files in walk(collect_root):
            found = set(imap(lambda file: join(pth, file),
                ifilter(lambda file: self.suffix_re.search(file, re.IGNORECASE), files)))
            self.collected |= found
    
    def collect_all(self):
        for directory in self.dirs:
            self.collect(directory)
    
    def parse(self, source):
        source_edit = (source,)
        for blockout_re in (self.quotes, self.dbl_quotes,
                            self.cpp_comments, self.c_comments):
            source_edit = blockout_re.subn(self.blockout, source_edit[0])
        try:
            sym = set(self.symbol_re.findall(source_edit[0]))
        except:
            sym = set()
        self.symbols |= sym - self.keywords
    
    def parse_file(self, file_name):
        self.pp("> Parsing source: %s" % file_name)
        self.parse(self.read(file_name))
    
    def parse_collected(self):
        for source_file in self.files:
            self.parse_file(source_file)
    
    @property
    def root(self):
        return getattr(self, 'rootdir', getcwd())
    
    @root.setter
    def root(self, root):
        if root == "CWD":
            root = abspath(getcwd())
        else:
            root = abspath(expanduser(root))
        if not isdir(root):
            raise IOError("Bad root dir: %s" % root)
        self.rootdir = root
    
    @property
    def suffixes(self):
        return getattr(self, 'sufs', SUFFIXES)
    
    @suffixes.setter
    def suffixes(self, sufs):
        if not hasattr(self, 'sufs'):
            self.sufs = set()
        if sufs:
            self.sufs |= sanitize_suffixes(*sufs)
    
    @property
    def directories(self):
        return tuple(getattr(self, 'dirs', set()))
    
    @directories.setter
    def directories(self, dirlist):
        self.dirs = set()
        if not dirlist:
            raise self.err("ERROR: Need to specify a directory to scan")
        for directory in dirlist:
            if isdir(abspath(directory)):
                self.dirs.add(abspath(directory))
            elif isdir(abspath(expanduser(directory))):
                self.dirs.add(abspath(expanduser(directory)))
            else:
                dd = abspath(join(self.root, directory))
                if isdir(dd):
                    self.dirs.add(dd)
                else:
                    self.pp("ERROR: Not a directory")
                    self.pp("\t%s" % directory)
    
    @property
    def files(self):
        return tuple(getattr(self, 'collected', set()))
    
    @property
    def symtab(self):
        return getattr(self, 'symbols', set())
    
    @property
    def values(self):
        return tuple(self.symtab)
    
    def __len__(self):
        return len(self.symtab)
    
    def __iter__(self):
        return self.values
    
    def __contains__(self, symbol):
        return symbol in self.symtab
    
    def next(self):
        if len(self) > 0:
            return self.values.next()
        raise StopIteration
