#!/bin/bash
# ==============================================================================
# = Submit LHE->Pool + Pool->Truth Ntuple to lxplus batch queue
# = This should be called from the BMinusLSUSY directort. It will create two
# = directories.
# =   jobs: hold job stearing files for the batch jobs - This can be discarded
# =         once jobs are completed
# =   d3pd: output ntuples will be copied here
# = usage: ./SubmitToBatch.sh <model dir> <model name> <queue>
# ==============================================================================

${DIR_ON_AFS_WORK}=${PWD}
sample_dir=$1
queue=$2

model_name=$(echo $sample_dir | sed "s#.*/##g")

echo "sample dir: $sample_dir"
echo "model name: $model_name"
echo "queue: $queue"

mkdir jobs

echo "#!/bin/bash" > jobs/jo_$model_name.sh
echo "" >> jobs/jo_$model_name.sh

echo "source ~/.bash_profile" >> jobs/jo_$model_name.sh
echo "" >> jobs/jo_$model_name.sh

echo "echo \"Copying files to worker node\"" >> jobs/jo_$model_name.sh
echo "cp -rf ${PWD}/../MadGraph5_v1_5_13 ." >> jobs/jo_$model_name.sh
echo "" >> jobs/jo_$model_name.sh

# Run MadGraph
echo "echo \"Running MadGraph\"" >> jobs/jo_$model_name.sh
echo "cd MadGraph5_v1_5_13" >> jobs/jo_$model_name.sh
echo "${PWD}/../TestConfig/RunTestProduction.sh $sample_dir" >> jobs/jo_$model_name.sh
echo "" >> jobs/jo_$model_name.sh

# Copy output to work space
echo "echo \"copying root files to work space\"" >> jobs/jo_$model_name.sh
echo "cp -rf $model_name $PWD" >> jobs/jo_$model_name.sh
echo "" >> jobs/jo_$model_name.sh

chmod +x jobs/jo_${model_name}.sh

echo "command"
cat jobs/jo_${model_name}.sh
echo ""

bsub -q $queue ${PWD}/jobs/jo_${model_name}.sh
