#!/bin/bash

# generate diagrams and set up MG5 area
./bin/mg5 ../SampleProcess.sh

# copy relevant files to Cards directory
cp ../SampleProcess/SampleProcess.slha Cards/param_card.dat
cp ../SampleProcess/pythia_card.dat    Cards/pythia_card.dat
cp ../SampleProcess/run_card.dat       Cards/run_card.dat

