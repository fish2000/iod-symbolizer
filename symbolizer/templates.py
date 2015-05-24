
from datetime import datetime

header_start_tpl = """
///
/// Generated by iod-symbolizer at %s
/// iod-symbolizer by Alexander Bohn -- http://github.com/fish2000/iod-symbolizer
/// IOD library by Matthieu Garrigues -- https://github.com/matt-42/iod
///

#include <iod/symbol.hh>

"""

header_num_symbol_tpl = """
#ifndef IOD_SYMBOL_%(symbol)s
    #define IOD_SYMBOL_%(symbol)s
    iod_define_number_symbol("%(symbol)s")
#endif

"""

header_std_symbol_tpl = """
#ifndef IOD_SYMBOL_%(symbol)s
    #define IOD_SYMBOL_%(symbol)s
    iod_define_symbol("%(symbol)s")
#endif

"""

def generate_header(symbol_set, when=None):
    if when is None:
        when is datetime.now().isoformat()
    
    header_out = header_start_tpl % when
    
    for symbol in symbol_set:
        try:
            int(symbol)
        except ValueError:
            # it's not a number
            header_out += header_std_symbol_tpl % dict(symbol=symbol)
        else:
            # ok, it's a number
            header_out += header_num_symbol_tpl % dict(symbol=symbol)
    
    return header_out