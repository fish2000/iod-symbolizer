#!/usr/bin/env python
# encoding: UTF-8

from __future__ import print_function

import unittest
import symbolizer

sample_input = unicode("""
// Copyright 2012-2014 Alexander Böhn <fish2000@gmail.com>
// License: MIT (see COPYING.MIT file)

#ifndef LIBIMREAD_IO_PNG_HH_
#define LIBIMREAD_IO_PNG_HH_

#include <cstring>
#include <csetjmp>
#include <vector>
#include <sstream>

#include <libimread/libimread.hpp>
#include <libimread/base.hh>
#include <libimread/options.hh>

namespace im {
    
    /*
    using namespace symbols::s;
    
    auto options =
    D(
        _compression_level     = -1,
        _backend               = "io_png"
    );
    */
    
    namespace PNG {
        
        struct format {
            
            static auto opts_init() {
                return D(
                    _signature = "\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"
                );
            }
            
            using options_type = decltype(format::opts_init());
            static const options_type options;
        };
        
    }
    
    #define PNG_SIGNATURE "\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"
    
    // namespace signature {
    //     struct PNGSignature {
    //         PNGSignature() {}
    //         operator char const*() { return "\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"; }
    //     };
    //     static const PNGSignature PNG;
    // }
    
    class PNGFormat : public ImageFormat {
        public:
            typedef std::true_type can_read;
            typedef std::true_type can_write;
            
            /// NOT AN OVERRIDE:
            static bool match_format(byte_source *src) {
                return match_magic(src, PNG_SIGNATURE, 8);
            }
            
            virtual std::unique_ptr<Image> read(byte_source *src,
                                                ImageFactory *factory,
                                                const options_map &opts) override;
            virtual void write(Image &input,
                               byte_sink *output,
                               const options_map &opts) override;
    };
    
    namespace format {
        using PNG = PNGFormat;
    }
    
}


#endif /// LIBIMREAD_IO_PNG_HH_
""", encoding='UTF-8', errors="replace").encode('UTF-8', errors="replace").strip()

sample_output = set(['compression_level', 'backend', 'signature'])

class SymbolizerTests(unittest.TestCase):
    
    def setUp(self):
        self.maxDiff = 1000
    
    def test_symbolize(self):
        source_edit = (sample_input,)
        for blockout_re in (symbolizer.quotes, symbolizer.dbl_quotes,
                            symbolizer.cpp_comments, symbolizer.c_comments):
            source_edit = blockout_re.subn(symbolizer.blockout, source_edit[0])
        try:
            sym = set(symbolizer.symbol_re.findall(source_edit[0])) - symbolizer.KEYWORDS
        except:
            sym = set()
        
        self.assertEqual(sym, sample_output)
    
    def test_file_read(self):
        pass

if __name__ == '__main__':
    unittest.main()
