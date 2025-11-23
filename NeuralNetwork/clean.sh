#!/bin/sh
ROOTDIR=`/bin/pwd`
for dir in `find . -type d -print`
do
    make -C "${dir}" -f "${ROOTDIR}"/Makefile clean
done
