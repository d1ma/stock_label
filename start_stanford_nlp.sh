#!/bin/bash

# exit on any failure
set -e

ctrlc() {
    cd ..
    exit
}

trap ctrlc SIGINT

cd stanfordnlp
python corenlp.py -P ../../stanford-corenlp-full-2014-08-27 -p 8091

