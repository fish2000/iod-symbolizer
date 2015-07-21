#!/usr/bin/env python
# encoding: UTF-8

import tempfile

input = unicode("""
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
    D(_compression_level     = -1,
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

output = set(['compression_level', 'backend', 'signature'])

header = """
///
/// Generated by iod-symbolizer at RIGHT NOW
/// iod-symbolizer by Alexander Bohn -- http://github.com/fish2000/iod-symbolizer
/// IOD library by Matthieu Garrigues -- https://github.com/matt-42/iod
///

#include <iod/symbol.hh>


#ifndef IOD_SYMBOL_signature
    #define IOD_SYMBOL_signature
    iod_define_symbol(signature)
#endif


#ifndef IOD_SYMBOL_compression_level
    #define IOD_SYMBOL_compression_level
    iod_define_symbol(compression_level)
#endif


#ifndef IOD_SYMBOL_backend
    #define IOD_SYMBOL_backend
    iod_define_symbol(backend)
#endif

"""

output_file = tempfile.NamedTemporaryFile(suffix='.hpp')
output_filename = output_file.name

arguments = {
    '--verbose':            True,
    '--root':               '~/Dropbox/libimread',
    '-o':                   output_filename,
    'DIR':                  ['include/libimread', 'src']
}

config = """

verbose: true
root: ~/Dropbox/libimread

source:
- src
- include/libimread

suffixes:       [c, cc, cpp, cxx, m, mm, h, hh, hpp, hxx, inl]
reserved:       [assert, raise, error, bridge, color_map]

target:
  file:       include/libimread/symbols.hpp
  overwrite:  true

"""
