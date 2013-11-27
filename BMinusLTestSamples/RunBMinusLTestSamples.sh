#!/bin/bash
# ==============================================================================
# = Simple script to produce diagrams for our model, then generate events using
# = MadGraph+Pythia
# = This should be called from within the MadGraph directory. Usage:
# =   ../BMinusLTestSamples/RunBMinusLTestSamples.sh
# ==============================================================================


for mass in 100 500 1000; do
  model_dir="BMinusLTestSamples"
  model_name="BMinusLTestSamples_$mass"

  # generate diagrams and set up MG5 area
  echo "Generating diagrams in MadGraph"
  ./bin/mg5 ../${model_dir}/Configure${model_name}.sh

  # copy relevant files to Cards directory
  echo "Copying files to Cards directory"
  cp ../${model_dir}/${model_name}.slha    ${model_name}/Cards/param_card.dat
  cp ../${model_dir}/pythia_card.dat       ${model_name}/Cards/pythia_card.dat
  cp ../${model_dir}/run_card.dat          ${model_name}/Cards/run_card.dat
  cp ../${model_dir}/me5_configuration.txt ${model_name}/Cards/me5_configuration.txt

  # move to model workspace
  cd ${model_name}

  # Generate events!
  #   This will run both MadGraph for the matrix element and Pythia for the decays
  #   and hadronization
  ./bin/generate_events -f --laststep=pythia
done
