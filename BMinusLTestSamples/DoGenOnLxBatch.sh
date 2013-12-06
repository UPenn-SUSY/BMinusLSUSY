#!/bin/bash
# ==============================================================================
# = usage: ./DoGenOnLxBatch.sh <DSID> <SHORT_NAME> <NUM_EVENTS> <QUEUE>
# ==============================================================================

# get variables from input
dsid=$1
short_name=$2
num_events=$3
queue=$4
dir_on_afs_work=${PWD}

pool_file_name="evgen.${dsid}.${short_name}.pool.root"
truth_ntuple_name="evgen.${dsid}.${short_name}.TRUTH.root"

echo "DSID: $dsid"
echo "Short name: $short_name"
echo "Num events: $num_events"
echo "Queue: $queue"
echo "Dir on afs work: ${dir_on_afs_work}"

mkdir jobs
mkdir samples
mkdir truth_d3pd

# make job option file
jo_file_name="jobs/jo.${dsid}.${short_name}.sh"
echo "#!/bin/bash" > $jo_file_name
echo "" >> $jo_file_name

# setup environment and athena
echo "# setup environment and athena" >> $jo_file_name
echo "source ~/.bash_profile" >> $jo_file_name
echo "source $AtlasSetup/scripts/asetup.sh 17.2.11.15,noTest,slc5,gcc43" >> $jo_file_name
echo 'export JOBOPTSEARCHPATH=/cvmfs/atlas.cern.ch/repo/sw/Generators/MC12JobOptions/latest/common:$JOBOPTSEARCHPATH' >> $jo_file_name
echo 'export JOBOPTSEARCHPATH=/cvmfs/atlas.cern.ch/repo/sw/Generators/MC12JobOptions/latest/susycontrol:$JOBOPTSEARCHPATH' >> $jo_file_name
echo "" >> $jo_file_name

# make directory for this sample
local_dir_name="${dsid}.${short_name}"
echo "# make directory for this sample - ${local_dir_name}" >> $jo_file_name
echo "mkdir ${local_dir_name}" >> $jo_file_name
echo "cd ${local_dir_name}" >> $jo_file_name
echo "" >> $jo_file_name

# copy files from afs
echo "# copy files from afs" >> $jo_file_name
echo "cp ${dir_on_afs_work}/configs/* . " >> $jo_file_name
echo "cp run_card.SM.dat run_card.dat" >> $jo_file_name
echo "" >> $jo_file_name

# Run generate trf
echo "# run generate trf" >> $jo_file_name
echo "Generate_trf.py runNumber=${dsid} randomSeed=1 firstEvent=1 jobConfig=MadGraphControl_SM_TT_directBL.py outputEVNTFile=${pool_file_name} ecmEnergy=8000 maxEvents=${num_events}" >> $jo_file_name
echo "" >> $jo_file_name

# Run reco trf
echo "# run reco trf" >> $jo_file_name
echo "Reco_trf.py inputEVNTFile=${pool_file_name} outputNTUP_TRUTHFile=${truth_ntuple_name}" >> $jo_file_name
echo "ls" >> $jo_file_name
echo "" >> $jo_file_name

# Copy dir to afs
echo "# Copy dir to afs" >> $jo_file_name
echo "cd .." >> $jo_file_name
echo "cp -r ${local_dir_name} ${dir_on_afs_work}/samples" >> $jo_file_name
echo "mv ${dir_on_afs_work}/samples/${local_dir_name}/${truth_ntuple_name} ${dir_on_afs_work}/truth_d3pd/${truth_ntuple_name}" >> $jo_file_name
echo "" >> $jo_file_name

# submit job to batch
chmod +x $jo_file_name
echo bsub -q ${queue} ${PWD}/${jo_file_name}
