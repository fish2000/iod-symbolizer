iod-symbolizer
==============

A parser for [IOD symbols](https://github.com/matt-42/iod), in C/C++/Objective-C/Objective-C++ source files. Given the following input:

```c++
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
```

... the `symbolizer` command will find the following symbols:

```c++
_compression_level
_backend
_signature
```

And by default, the generated header file will look like so:

```c++
///
/// Generated by iod-symbolizer at 2015-05-24T05:02:20.448982
/// iod-symbolizer by Alexander Bohn -- http://github.com/fish2000/iod-symbolizer
/// IOD library by Matthieu Garrigues -- https://github.com/matt-42/iod
///

#include <iod/symbol.hh>


#ifndef IOD_SYMBOL_assert
    #define IOD_SYMBOL_assert
    iod_define_symbol(assert)
#endif


#ifndef IOD_SYMBOL_color_map
    #define IOD_SYMBOL_color_map
    iod_define_symbol(color_map)
#endif


#ifndef IOD_SYMBOL_compression_level
    #define IOD_SYMBOL_compression_level
    iod_define_symbol(compression_level)
#endif


#ifndef IOD_SYMBOL_x_
    #define IOD_SYMBOL_x_
    iod_define_symbol(x_)
#endif


#ifndef IOD_SYMBOL_signature
    #define IOD_SYMBOL_signature
    iod_define_symbol(signature)
#endif


#ifndef IOD_SYMBOL_fd
    #define IOD_SYMBOL_fd
    iod_define_symbol(fd)
#endif


#ifndef IOD_SYMBOL_pitch
    #define IOD_SYMBOL_pitch
    iod_define_symbol(pitch)
#endif


#ifndef IOD_SYMBOL_backend
    #define IOD_SYMBOL_backend
    iod_define_symbol(backend)
#endif
```

By default, the generated header is written to STDOUT. Run the symbolizer like so to write to a specific file:

```bash
$ symbolizer DIR0 DIR1 DIR2 -o symbols.hh
```

Install
-------

Install with Pip, via PyPI:

```bash
$ pip install -U iod-symbolizer
```

… Or via GitHub:

```bash
$ git clone https://github.com/fish2000/iod-symbolizer.git
$ cd iod-symbolizer
$ pip install -U -r requirements.txt
$ pip install -U .
```

Questions?
----------

Contact me, I welcome all inquiries: fish2000, at the geemail, etc etc. I am also available for hire!
