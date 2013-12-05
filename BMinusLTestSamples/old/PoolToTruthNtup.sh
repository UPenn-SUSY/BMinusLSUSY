#!/bin/bash
# ==============================================================================
# = Convert Pool file to Truth Ntuple
# = This assumes you are running in the same directory as your pool file
# = usage: ./PoolToTruthNtup.sh <out file short>
# ==============================================================================

# get input/output file names
OUT_FILE_SHORT=$1
if [[ $OUT_FILE_SHORT == "" ]]; then
  OUT_FILE_SHORT="BMinusLTestSamples"
fi
echo "OUT_FILE_SHORT: ${OUT_FILE_SHORT}"

Reco_trf.py inputEVNTFile=evgen.${OUT_FILE_SHORT}_pool.root \
            outputNTUP_TRUTHFile=evgen.${OUT_FILE_SHORT}.TRUTH.root
