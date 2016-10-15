from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

from parser import (
    SUFFIXES, KEYWORDS, SYMBOL_PREFIX,
    sanitizer, symbol_re, suffix_re,
    quotes, dbl_quotes, cpp_comments, c_comments, blockout,
    collect_files, sanitize_suffixes, collect,
    parse, parse_source_file)

from parser import Parser
from templates import (
    generate_header,
    u as symbolizer_unicode)