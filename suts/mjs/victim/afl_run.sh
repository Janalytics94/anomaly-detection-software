#!/bin/bash

cd mjs-issues-57; git checkout d6c06a6
export AFL="/afl"
mkdir in; echo "" > in/in
$AFL/afl-fuzz -m none -i in -o out ./mjs-bin -f @@