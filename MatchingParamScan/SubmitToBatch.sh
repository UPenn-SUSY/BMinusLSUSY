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
stop_mass=$1
xqcut=$2
qcut=$3
queue=$4

model_name="mstop_${stop_mass}__xqcut_${xqcut}__qcut_${qcut}"

echo "stop mass: $stop_mass"
echo "xqcut: $xqcut"
echo "qcut: $qcut"
echo "queue: $queue"

mkdir jobs

mkdir $model_name
cp CreateCard.py Reference*Card.dat $model_name

echo "#!/bin/bash" > jobs/jo__$model_name.sh
echo "" >> jobs/jo__$model_name.sh

echo "source ~/.bash_profile" >> jobs/jo__$model_name.sh
echo "" >> jobs/jo__$model_name.sh

echo "echo \"Copying files to worker node\"" >> jobs/jo__$model_name.sh
echo "cp -rf ${PWD}/../MadGraph5_v1_5_13 ." >> jobs/jo__$model_name.sh
echo "cp ${PWD}/$model_name/CreateCard.py ." >> jobs/jo__$model_name.sh
echo "cp ${PWD}/$model_name/Reference*Card.dat ." >> jobs/jo__$model_name.sh
echo "" >> jobs/jo__$model_name.sh

# echo "echo \"Creating cards\"" >> jobs/jo__$model_name.sh
# echo "./CreateCard.py ReferenceParamCard.dat param_card.dat M_STOP $stop_mass" >> jobs/jo__$model_name.sh
# echo "./CreateCard.py ReferencePythiaCard.dat pythia_card.dat QCUT $qcut" >> jobs/jo__$model_name.sh
# echo "./CreateCard.py ReferenceRunCard.dat run_card.dat XQCUT $xqcut" >> jobs/jo__$model_name.sh
# echo "" >> jobs/jo__$model_name.sh

# Run MadGraph
echo "echo \"Running MadGraph\"" >> jobs/jo__$model_name.sh
echo "cd MadGraph5_v1_5_13" >> jobs/jo__$model_name.sh
echo "${PWD}/RunTestProduction.sh ${PWD}/${model_name} ${stop_mass} ${xqcut} ${qcut}" >> jobs/jo__$model_name.sh
echo "" >> jobs/jo__$model_name.sh

# Copy output to work space
echo "echo \"copying cards to work space\"" >> jobs/jo__$model_name.sh
echo "cp *_card.dat $PWD/${model_name}" >> jobs/jo__$model_name.sh
echo "" >> jobs/jo__$model_name.sh
echo "echo \"copying jet matching plots to work space\"" >> jobs/jo__$model_name.sh
# echo "cp -rf *_card.dat $PWD/${model_name}" >> jobs/jo__$model_name.sh
# 
chmod +x jobs/jo__${model_name}.sh

echo "command"
cat jobs/jo__${model_name}.sh
echo ""

echo bsub -q $queue ${PWD}/jobs/jo__${model_name}.sh
