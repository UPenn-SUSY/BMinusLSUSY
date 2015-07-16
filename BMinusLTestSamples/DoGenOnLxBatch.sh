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

# make config file name
config_file_name="MC15.${dsid}.MGPy8EG_${short_name}.py"

# make job option file
jo_file_name="jobs/jo.${dsid}.${short_name}.sh"
echo "#!/bin/bash" > $jo_file_name
echo "" >> $jo_file_name

# setup environment and athena
echo "# setup environment and athena" >> $jo_file_name
echo 'LOCAL_WORK_DIR=${PWD}' >> $jo_file_name
echo "source ~/.bash_profile" >> $jo_file_name
# echo "cd ${TestArea}" >> $jo_file_name
echo "source ${AtlasSetup}/scripts/asetup.sh 19.2.4.4.2,MCProd,slc6,gcc47" >> $jo_file_name
echo 'cd ${LOCAL_WORK_DIR}' >> $jo_file_name
echo "" >> $jo_file_name

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
echo "echo \
\"include('MadGraphControl_SM_TT_directBL.mg_stop__pythia_decay.py')\" \
> ${config_file_name}" >> $jo_file_name
echo "" >> $jo_file_name

# Run generate tf
echo "# run generate tf" >> $jo_file_name
echo "Generate_tf.py \
--runNumber=${dsid} \
--randomSeed=1 \
--firstEvent=1 \
--jobConfig=${config_file_name} \
--outputEVNTFile=${pool_file_name} \
--ecmEnergy=${com_energy} \
--maxEvents=${num_events}" \
>> $jo_file_name
echo "" >> $jo_file_name

# change release for reco tf
echo "source \
/afs/cern.ch/atlas/software/dist/AtlasSetup/scripts/asetup.sh 20.1.5.4,AtlasDerivation,slc6,gcc48" \
>> $jo_file_name
echo "" >> $jo_file_name

# Run reco tf
echo "# run reco tf" >> $jo_file_name
# echo "Reco_trf.py inputEVNTFile=${pool_file_name} \
# outputNTUP_TRUTHFile=${truth_ntuple_name}" >> $jo_file_name
echo "Reco_tf.py --inputEVNTFile ${pool_file_name} \
--outputDAODFile ${truth_ntuple_name} \
--reductionConf TRUTH1" >> $jo_file_name
echo "ls" >> $jo_file_name
echo "" >> $jo_file_name

# Clean up big files before copying
echo "rm *.events" >> $jo_file_name
echo "rm events.lhe" >> $jo_file_name
echo "rm evgen.*.pool.root" >> $jo_file_name
echo "rm -rf PROC_ReducedUFO_0" >> $jo_file_name
echo "" >> $jo_file_name

# Copy dir to afs
echo "# Copy dir to afs" >> $jo_file_name
echo "cd .." >> $jo_file_name
echo "cp -r ${local_dir_name} ${dir_on_afs_work}/samples" >> $jo_file_name
echo "mv ${dir_on_afs_work}/samples/${local_dir_name}/DAOD_TRUTH1.${truth_ntuple_name} \
${dir_on_afs_work}/truth_d3pd/DAOD_TRUTH1.${truth_ntuple_name}" >> $jo_file_name
echo "" >> $jo_file_name

# submit job to batch
chmod +x $jo_file_name
echo bsub -q ${queue} ${PWD}/${jo_file_name}
