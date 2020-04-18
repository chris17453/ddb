# coding: utf8
import sys

utf8str='╔════════════════════════════════════╗'


def mprint(Text):
    
    if sys.version_info.major==2:
        sys.stdout.write(Text)
    elif sys.version_info.major==3:
        # DIRECT BUFFER, std out wont let you do this
        # the buffer takes direct byte, like writing to the screen directly
        sys.stdout.buffer.write(utf8str.encode('utf-8'))

mprint(utf8str)