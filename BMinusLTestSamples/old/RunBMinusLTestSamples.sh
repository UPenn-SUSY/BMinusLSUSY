#!/bin/bash
# ==============================================================================
# = Simple script to produce diagrams for our model, then generate events using
# = MadGraph+Pythia
# = This should be called from within the MadGraph directory. Usage:
# =   ../BMinusLTestSamples/RunBMinusLTestSamples.sh
# ==============================================================================

rel_path=$(echo $0 | sed "s#RunBMinusLTestSamples.sh##g")
echo $rel_path
model_dir="BMinusLTestSamples"

for mass in 100 500 1000; do
  for njets in 0 1 ; do
    echo ''
    model_name="${model_dir}_${mass}_np${njets}"
    param_card_name="${model_dir}_${mass}"

    # generate madgraph config file
    ./$rel_path/GenerateMadGraphConfig.py --model-dir=${model_dir} \
                                          --stop-mass=${mass} \
                                          --num-partons=${njets} 

    # generate diagrams and set up MG5 area
    echo "Generating diagrams in MadGraph"
    ./bin/mg5 config_${model_name}.sh

    # copy relevant files to Cards directory
    echo "Copying files to Cards directory"
    cp ./${rel_path}/${param_card_name}.slha ${model_name}/Cards/param_card.dat
    cp ./${rel_path}/pythia_card.dat         ${model_name}/Cards/pythia_card.dat
    if [[ $njets == "0" ]] ; then
      cp ./${rel_path}/run_card_wojets.dat   ${model_name}/Cards/run_card.dat
    else
      cp ./${rel_path}/run_card_wjets.dat    ${model_name}/Cards/run_card.dat
    fi
    cp ./${rel_path}/me5_configuration.txt   ${model_name}/Cards/me5_configuration.txt

    sed -i "s#CONFIGURE_PATH#${PWD}#g" ${model_name}/Cards/me5_configuration.txt

    # move to model workspace
    cd ${model_name}

    # Generate events!
    #   This will run just the matrix elemetn in MadGraph
    # ./bin/generate_events -f
    # If you want to do both the matrix element (MadGraph) and the
    #   decays/hadronization, use this command instead.
    # ./bin/generate_events -f --laststep=pythia

    cd ..
  done
done
