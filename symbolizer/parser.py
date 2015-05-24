#!/usr/bin/env python

from __future__ import print_function

import re
import functools
from itertools import ifilter, imap
from os.path import join, expanduser, abspath, isdir, isabs
from os import walk, getcwd

SUFFIXES = set((
    r"c",
    r"cc", r"cpp", r"cxx",
    r"m", r"mm",
    r"h",
    r"hh", r"hpp", r"hxx",
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
# symbol_re = re.compile(r"(?:\w+)%s([a-zA-Z][0-9a-zA-Z_]+)(?!_t)" % SYMBOL_PREFIX)
symbol_re = re.compile(r"(?:\s+)(?:%s)([0-9a-z][0-9a-z_]+)(?!_t)" % SYMBOL_PREFIX)
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
    return set((sanitizer.sub('', suffix.lower()) for suffix in suffixes))

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

class Parser(object):
    
    quotes          = re.compile(r"'(.*)'",     re.MULTILINE)
    dbl_quotes      = re.compile(r'"(.*)"',     re.MULTILINE)
    cpp_comments    = re.compile(r'//(.*)\n',   re.MULTILINE)
    c_comments      = re.compile(r'/\*(.*)\*/', re.MULTILINE)
    blockout        = lambda match: "#" * len(match.group(0))
    
    def __init__(self, *args, **arguments):
        super(Parser, self).__init__(args, arguments)
        
        self.suffixes = SUFFIXES
        self.keywords = KEYWORDS
        self.dirs = set()
        self.collected = set()
        self.symbols = set()
        self.symbol_re = re.compile(
            r"(?:\s+)(?:%s)([0-9a-z][0-9a-z_]+)(?!_t)" % SYMBOL_PREFIX)
        
        self.verbose = arguments.pop('--verbose', False)
        
        symbolize_opts = dict(
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
            r"(?:\s+)(?:%s)([%s][%s]+)(?!_t)" % (
                SYMBOL_PREFIX,
                symbol_init_range,
                symbol_main_range))
        
        suffixes = arguments.pop('--suffixes', None)
        if suffixes:
            self.suffixes = sanitize_suffixes(suffixes)
        
        self.suffix_re = re.compile(r"(%s)$" % ("|".join(map(
            lambda suffix: r"\.%s" % suffix, self.suffixes))))
        
        root = arguments.pop('--root')
        if root == "CWD":
            root = abspath(getcwd())
        else:
            root = abspath(root)
        if not isdir(root):
            raise IOError("Bad root dir: %s" % root)
        
        for directory in arguments['DIR']:
            if isabs(directory):
                self.dirs.add(directory)
            else:
                dd = join(root, directory)
                if isdir(dd):
                    self.dirs.add(dd)
                else:
                    raise IOError("DIR WTF: %s" % dd)
    
    def collect(self, root_dir):
        for pth, dirs, files in walk(expanduser(root_dir)):
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
    
    def parse_source_file(self, file_name):
        with open(file_name, "rb") as fh:
            source_file = fh.read()
        self.parse(source_file)
    
    def parse_collected(self):
        for source_file in self.collected:
            self.parse_source_file(source_file)
    
    def __len__(self):
        return len(self.symbols)
    
    @property
    def directories(self):
        return tuple(self.symbols)
    
    @property
    def files(self):
        return tuple(self.collected)
    
    @property
    def symbols(self):
        return tuple(self.symbols)

