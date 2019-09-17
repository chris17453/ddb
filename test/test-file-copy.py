#!/usr/bin/python

import os,sys

def copy(src,dst):
    BUFFER_SIZE=1004
    SRC_FLAGS =  os.O_RDONLY 
    DST_FLAGS = os.O_CREAT |  os.O_TRUNC | os.O_WRONLY  | os.O_SYNC 
    src_fd = os.open(src, SRC_FLAGS)
    dst_fd = os.open(dst, DST_FLAGS)

    print src_fd
    print dst_fd
    while True:
        fb_1=os.read(src_fd,BUFFER_SIZE)
        if fb_1=='':
            break
        os.write(dst_fd, fb_1)

    if src_fd:
        os.close(src_fd)
    if dst_fd:
        os.close(dst_fd)

src="/home/cwatkin1/repos/chris17453/ddb/test/data/MOCK_DATA.csv"
dst="/home/cwatkin1/repos/chris17453/ddb/test/data/MOCK_DATA.csv2"



copy(src,dst)