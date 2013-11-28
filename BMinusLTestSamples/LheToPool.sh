#!/bin/bash
# ==============================================================================
# = Convert LHE file to Pool file
# = usage: ./LheToPool.sh <Location of LHE file> <out file short>
# ==============================================================================

# get input/output file names
IN_FILE=$1
OUT_FILE_SHORT="$2"
if [[ $OUT_FILE_SHORT == "" ]]; then
  OUT_FILE_SHORT="BMinusLTestSamples"
fi
FORMATED_LHE_NAME="${OUT_FILE_SHORT}_unweighted_events.lhe._000001.events"

"IN_FILE: ${IN_FILE}"
"OUT_FILE_SHORT: ${OUT_FILE_SHORT}"
"FORMATED_LHE_NAME: ${FORMATED_LHE_NAME}"

# move lhe file to convenient location & untar
cp ${IN_FILE} ${FORMATED_LHE_NAME}
tar -cvzf ${FORMATED_LHE_NAME}.tar.gz ${FORMATED_LHE_NAME}

# generate pool file
Generate_trf.py ecmEnergy=8000 \
                runNumber=1 \
                firstEvent=1 \
                maxEvents=10 \
                randomSeed=400010  \
                jobConfig=../testlhe.py  \
                outputEVNTFile=evgen.${OUT_FILE_SHORT}_pool.root  \
                inputGeneratorFile=${FORMATED_LHE_NAME}.tar.gz 

                # maxEvents=-1 \

mv Generate.log ${OUT_FILE_SHORT}.log
