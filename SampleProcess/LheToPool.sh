#!/bin/bash

# get input/output file names
IN_FILE=$1
OUT_FILE_SHORT="SampleProcess"
FORMATED_LHE_NAME="${OUT_FILE_SHORT}_unweighted_events.lhe._000001.events"

# move lhe file to convenient location & untar
cp ${IN_FILE} ${FORMATED_LHE_NAME}.gz
gunzip ${IN_FILE} ${FORMATED_LHE_NAME}.gz
echo tar -cvzf ${FORMATED_LHE_NAME}.tar.gz ${FORMATED_LHE_NAME}

# # get set up
# # TODO move this to another script
# asetup AtlasProduction,17.2.8.3
export JOBOPTSEARCHPATH=/cvmfs/atlas.cern.ch/repo/sw/Generators/MC12JobOptions/latest/common:$JOBOPTSEARCHPATH

# generate 
echo Generate_trf.py ecmEnergy=8000 \
                runNumber=1 \
                firstEvent=1 \
                maxEvents=-1 \
                randomSeed=400010  \
                jobConfig=testlhe.py  \
                outputEVNTFile=evgen.${OUT_FILE_SHORT}_pool.root  \
                inputGeneratorFile=${FORMATED_LHE_NAME}.tar.gz 

# mv Generate.log ${OUT_FILE_SHORT}.log

# Reco_trf.py inputEVNTFile=evgen.SampleProcess_pool.root outputNTUP_TRUTHFile=evgen.lllpv_012p_00_TRUTH.root
