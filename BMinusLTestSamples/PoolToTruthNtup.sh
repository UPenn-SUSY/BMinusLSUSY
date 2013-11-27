#!/bin/bash

# get input/output file names
# IN_FILE=$1
OUT_FILE_SHORT=$1
if [[ $OUT_FILE_SHORT == "" ]]; then
  OUT_FILE_SHORT="BMinusLTestSamples"
fi

Reco_trf.py inputEVNTFile=evgen.${OUT_FILE_SHORT}_pool.root \
            outputNTUP_TRUTHFile=evgen.${OUT_FILE_SHORT}.TRUTH.root
