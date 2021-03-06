#!/bin/bash
# ==============================================================================
# = Simple script to produce diagrams for our model, then generate events using
# = MadGraph+Pythia
# = This should be called from within the MadGraph directory. Usage:
# =   ../BMinusLTestSamples/RunBMinusLTestSamples.sh
# ==============================================================================

sample_path=$1
rel_path=$(echo $0 | sed "s#RunTestProduction.sh##g")
# echo $rel_path
# model_dir="BMinusLTestSamples"

model_name=$(echo $sample_path | sed "s#.*/##g")

echo "sample path: $sample_path"
echo "model: $model_name"

# generate madgraph config file
$rel_path/ConfigureModel.sh $model_name

# generate diagrams and set up mg5 area
echo "Generating diagrams in MadGraph"
./bin/mg5 config_${model_name}.sh

# copy relevant files to Cards directory
echo "Copying files to Cards directory"
cp ${sample_path}/param_card.dat  ${model_name}/Cards/param_card.dat
cp ${sample_path}/pythia_card.dat ${model_name}/Cards/pythia_card.dat
cp ${sample_path}/run_card.dat    ${model_name}/Cards/run_card.dat

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

#     model_name="${model_dir}_${mass}_np${njets}"
#     param_card_name="${model_dir}_${mass}"
# 
#     # generate madgraph config file
#     ./$rel_path/GenerateMadGraphConfig.py --model-dir=${model_dir} \
#                                           --stop-mass=${mass} \
#                                           --num-partons=${njets} 
# 
#     # generate diagrams and set up MG5 area
#     echo "Generating diagrams in MadGraph"
#     ./bin/mg5 config_${model_name}.sh
# 
#     # copy relevant files to Cards directory
#     echo "Copying files to Cards directory"
#     cp ./${rel_path}/${param_card_name}.slha ${model_name}/Cards/param_card.dat
#     cp ./${rel_path}/pythia_card.dat         ${model_name}/Cards/pythia_card.dat
#     if [[ $njets == "0" ]] ; then
#       cp ./${rel_path}/run_card_wojets.dat   ${model_name}/Cards/run_card.dat
#     else
#       cp ./${rel_path}/run_card_wjets.dat    ${model_name}/Cards/run_card.dat
#     fi
#     cp ./${rel_path}/me5_configuration.txt   ${model_name}/Cards/me5_configuration.txt
# 
#     sed -i "s#CONFIGURE_PATH#${PWD}#g" ${model_name}/Cards/me5_configuration.txt
# 
#     # move to model workspace
#     cd ${model_name}
# 
#     # Generate events!
#     #   This will run just the matrix elemetn in MadGraph
#     # ./bin/generate_events -f
#     # If you want to do both the matrix element (MadGraph) and the
#     #   decays/hadronization, use this command instead.
#     # ./bin/generate_events -f --laststep=pythia
# 
#     cd ..
#   done
# done
