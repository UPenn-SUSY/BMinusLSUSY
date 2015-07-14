#!/bin/bash
# ==============================================================================
# = usage: ./DoGenOnLxBatch.sh <DSID> <SHORT_NAME> <QUEUE> <leptons_in_decay> <decay_stops_in_mg> <num_additional_partons> <com_energy>
# ==============================================================================

# get variables from input
dsid=$1
short_name=$2
num_events=-1
queue=$3
dir_on_afs_work=${PWD}
leptons_in_decay=$4
decay_stops_in_mg=$5
num_additional_partons=$6
com_energy=$7

# check for valid queue name
if [[ "$queue" == "" ]] ; then
  # default to 8nh
  queue="8nh"
fi

# check for valid leptons in decay
if [[ "$leptons_in_decay" == "" ]] ; then
  # default to e+mu only
  leptons_in_decay="em"
fi

# check for valid decay stops in MG option
if [[ "$decay_stops_in_mg" == "" ]] ; then
  # default to no
  decay_stops_in_mg="0"
fi

# check valid number of additional partons
if [[ "$num_additional_partons" == "" ]] ; then
  # default to 0
  num_additional_partons="0"
fi

# check for valid com energy
if [[ "$com_energy" == "" ]] ; then
  com_energy=8000
fi

pool_file_name="evgen.${dsid}.${short_name}.pool.root"
truth_ntuple_name="evgen.${dsid}.${short_name}.com_e_${com_energy}.TRUTH.root"

echo "DSID: $dsid"
echo "Short name: $short_name"
echo "Num events: $num_events"
echo "Queue: $queue"
echo "Dir on afs work: ${dir_on_afs_work}"
echo "leptons in decay: ${leptons_in_decay}"
echo "Decay stops in MG: ${decay_stops_in_mg}"
echo "Number additional partons: ${num_additional_partons}"

if [[ ! -d jobs ]]; then
  mkdir jobs
fi
if [[ ! -d samples ]]; then
  mkdir samples
fi
if [[ ! -d truth_d3pd ]]; then
  mkdir truth_d3pd
fi

# make job option file
jo_file_name="jobs/jo.${dsid}.${short_name}.sh"
echo "#!/bin/bash" > $jo_file_name
echo "" >> $jo_file_name

# setup environment and athena
echo "# setup environment and athena" >> $jo_file_name
echo 'LOCAL_WORK_DIR=${PWD}' >> $jo_file_name
echo "source ~/.bash_profile" >> $jo_file_name
# echo "cd ${TestArea}" >> $jo_file_name
echo "source ${AtlasSetup}/scripts/asetup.sh 20.1.4.14,slc6,gcc48" >> $jo_file_name
# echo 'export JOBOPTSEARCHPATH=/cvmfs/atlas.cern.ch/repo/sw/Generators/MC12JobOptions/latest/common:$JOBOPTSEARCHPATH' >> $jo_file_name
# echo 'export JOBOPTSEARCHPATH=/cvmfs/atlas.cern.ch/repo/sw/Generators/MC12JobOptions/latest/susycontrol:$JOBOPTSEARCHPATH' >> $jo_file_name
echo 'cd ${LOCAL_WORK_DIR}' >> $jo_file_name
echo "" >> $jo_file_name

# # Copy MadGraph to local directory
# echo "# copy MadGraph to local directory" >> $jo_file_name
# # make this more robust to pwd when calling script
# echo "cp -r ${PWD}/../MadGraph5_v1_5_12 ." >> $jo_file_name
# echo 'MADPATH=${PWD}/MadGraph5_v1_5_12' >> $jo_file_name
# echo "" >> $jo_file_name

# make directory for this sample
local_dir_name="${dsid}.${short_name}.com_e_${com_energy}"
echo "# make directory for this sample - ${local_dir_name}" >> $jo_file_name
echo "mkdir ${local_dir_name}" >> $jo_file_name
echo "cd ${local_dir_name}" >> $jo_file_name
echo "" >> $jo_file_name

# copy files from afs
echo "# copy files from afs" >> $jo_file_name
echo "cp ${dir_on_afs_work}/configs/* . " >> $jo_file_name
echo "" >> $jo_file_name

# pick correct parameter card
echo "# picking correct parameter card" >> $jo_file_name
echo "cp param_card.SM.TT.directBL__${leptons_in_decay}.dat param_card.SM.TT.directBL.dat" >> $jo_file_name
# fi
echo "" >> $jo_file_name

# pick correct MadGraphControl script
echo "# picking correct MadGraphControl script" >> $jo_file_name
if [[ "$decay_stops_in_mg" == "1" ]] ; then
  if [[ "$num_additional_partons" == "1" ]] ; then
    echo "cp MadGraphControl_SM_TT_directBL.mg_stop__mg_decay.py MadGraphControl_SM_TT_directBL.py" >> $jo_file_name
  elif [[ "$num_additional_partons" == "0" ]] ; then
    echo "cp MadGraphControl_SM_TT_directBL.np0.mg_stop__mg_decay.py MadGraphControl_SM_TT_directBL.py" >> $jo_file_name
  fi
else
  if [[ "$num_additional_partons" == "1" ]] ; then
    echo "cp MadGraphControl_SM_TT_directBL.mg_stop__pythia_decay.py MadGraphControl_SM_TT_directBL.py" >> $jo_file_name
  elif [[ "$num_additional_partons" == "0" ]] ; then
    echo "cp MadGraphControl_SM_TT_directBL.np0.mg_stop__pythia_decay.py MadGraphControl_SM_TT_directBL.py" >> $jo_file_name
  fi
fi
echo "" >> $jo_file_name

# Run generate trf
echo "# run generate trf" >> $jo_file_name
## echo "Generate_trf.py runNumber=${dsid} randomSeed=1 firstEvent=1 jobConfig=MadGraphControl_SM_TT_directBL.py outputEVNTFile=${pool_file_name} ecmEnergy=8000 maxEvents=${num_events}" >> $jo_file_name
# echo "Generate_trf.py runNumber=${dsid} randomSeed=1 firstEvent=1 jobConfig=MadGraphControl_SM_TT_directBL.py outputEVNTFile=${pool_file_name} ecmEnergy=${com_energy} maxEvents=${num_events}" >> $jo_file_name
echo "Generate_tf.py \
--runNumber=${dsid} \
--randomSeed=1 \
--firstEvent=1 \
--jobConfig=MadGraphControl_SM_TT_directBL.py \
--outputEVNTFile=${pool_file_name} \
--ecmEnergy=${com_energy} \
--maxEvents=${num_events}" \
>> $jo_file_name
echo "" >> $jo_file_name

# Run reco trf
echo "# run reco trf" >> $jo_file_name
echo "Reco_trf.py inputEVNTFile=${pool_file_name} outputNTUP_TRUTHFile=${truth_ntuple_name}" >> $jo_file_name
echo "ls" >> $jo_file_name
echo "" >> $jo_file_name

# Clean up big files before copying
echo "rm madgraph.202632.madgraph_SM_TT_directBL_100._00001.events" >> $jo_file_name
echo "rm events.lhe" >> $jo_file_name
echo "rm evgen.*.pool.root" >> $jo_file_name
echo "rm -rf PROC_ReducedUFO_0" >> $jo_file_name
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
