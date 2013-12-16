#!/bin/bash
# ==============================================================================
# = Simple script to produce diagrams for our model, then generate events using
# = MadGraph+Pythia
# = This should be called from within the MadGraph directory. Usage:
# =   ../BMinusLTestSamples/RunBMinusLTestSamples.sh
# ==============================================================================

sample_path=$1
stop_mass=$2
xqcut=$3
qcut=$4

rel_path=$(echo $0 | sed "s#RunTestProduction.sh##g")
model_name=$(echo $sample_path | sed "s#.*/##g")

echo "sample path: $sample_path"
echo "model: $model_name"
echo "stop mass: $stop_mass"
echo "xqcut: $xqcut"
echo "qcut: $qcut"

# generate madgraph config file
$rel_path/ConfigureModel.sh $model_name

# generate diagrams and set up mg5 area
echo "Generating diagrams in MadGraph"
./bin/mg5 config__${model_name}.sh

# copy relevant files to Cards directory
echo "Copying files to Cards directory"
${sample_path}/CreateCard.py ${sample_path}/ReferenceParamCard.dat ${model_name}/Cards/param_card.dat M_STOP $stop_mass
${sample_path}/CreateCard.py ${sample_path}/ReferenceRunCard.dat ${model_name}/Cards/run_card.dat XQCUT $xqcut
${sample_path}/CreateCard.py ${sample_path}/ReferencePythiaCard.dat ${model_name}/Cards/pythia_card.dat QCUT $qcut

# cp ${sample_path}/param_card.dat  ${model_name}/Cards/param_card.dat
# cp ${sample_path}/pythia_card.dat ${model_name}/Cards/pythia_card.dat
# cp ${sample_path}/run_card.dat    ${model_name}/Cards/run_card.dat

# cp ./${rel_path}/me5_configuration.txt   ${model_name}/Cards/me5_configuration.txt
# sed -i "s#CONFIGURE_PATH#${PWD}#g" ${model_name}/Cards/me5_configuration.txt

# move to model workspace
cd ${model_name}

# Generate events!
#   This will run just the matrix elemetn in MadGraph
# ./bin/generate_events -f
# If you want to do both the matrix element (MadGraph) and the
#   decays/hadronization, use this command instead.
# ./bin/generate_events -f --laststep=pythia
./bin/generate_events
