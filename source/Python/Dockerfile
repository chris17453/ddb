# Author: Charles Watkins
# Desc: builds a static python binary for use with embedding in compiled python scripts.
# ex a single static exe, no deps 
FROM centos:7

volume /transfer

RUN yum install make gcc gcc-c++ yum-utils glibc-static wget tar -y
RUN yum-builddep python -y
RUN wget https://www.python.org/ftp/python/2.7.16/Python-2.7.16.tgz 
RUN tar -xzvf Python-2.7.16.tgz  
RUN rm Python-2.7.16.tgz
WORKDIR /Python-2.7.16

COPY Python-2.7.16/Setup Modules/Setup
RUN mkdir bin

RUN ./configure     --disable-shared \
                    --enable-profiling \
                    --enable-optimizations\
                    --prefix="/python" \
                    LDFLAGS="-Wl,-no-export-dynamic -static -static-libgcc" \
                    CPPFLAGS="-static -fPIC" \
                    LINKFORSHARED=" " \
                    DYNLOADFILE="dynload_stub.o"

                    

RUN make
RUN make altinstall
#ENTRYPOINT ['/usr/bin/cp','-r ','/python/*','/transfer/']

#Failed to build these modules:
#_bsddb             _codecs_cn         _codecs_hk      
#_codecs_iso2022    _codecs_jp         _codecs_kr      
#_codecs_tw         _ctypes            _ctypes_test    
#_curses            _curses_panel      _hashlib        
#_hotshot           _json              _lsprof         
#_multibytecodec    _multiprocessing   _socket         
#_sqlite3           _ssl               _tkinter        
#audioop            bz2                crypt           
#dbm                future_builtins    gdbm            
#linuxaudiodev      nis                ossaudiodev     
#pyexpat            readline           resource        
#termios            zlib                               
