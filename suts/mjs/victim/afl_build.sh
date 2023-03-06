#!/bin/bash

cd mjs-issues-57; git checkout d6c06a6
export AFL="/afl"
export SUBJECT=$PWD; export TMP_DIR=$PWD/obj-aflgo/temp
export CC=$AFL/afl-gcc
export LDFLAGS=-lpthread
export ADDITIONAL="-fPIC"

$CC -DMJS_MAIN mjs.c -ldl -g -o mjs-bin