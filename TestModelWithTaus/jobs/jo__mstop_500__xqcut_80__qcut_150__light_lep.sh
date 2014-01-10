#!/bin/bash

source ~/.bash_profile

echo "Copying files to worker node"
cp -rf /afs/cern.ch/user/b/bjackson/work/public/BMinusLSUSY_Generation/BMinusLSUSY/TestModelWithTaus/../MadGraph5_v1_5_13 .
cp /afs/cern.ch/user/b/bjackson/work/public/BMinusLSUSY_Generation/BMinusLSUSY/TestModelWithTaus/mstop_500__xqcut_80__qcut_150__light_lep/CreateCard.py .
cp /afs/cern.ch/user/b/bjackson/work/public/BMinusLSUSY_Generation/BMinusLSUSY/TestModelWithTaus/mstop_500__xqcut_80__qcut_150__light_lep/Reference*Card.dat .

echo "Running MadGraph"
cd MadGraph5_v1_5_13
/afs/cern.ch/user/b/bjackson/work/public/BMinusLSUSY_Generation/BMinusLSUSY/TestModelWithTaus/RunTestProduction.sh /afs/cern.ch/user/b/bjackson/work/public/BMinusLSUSY_Generation/BMinusLSUSY/TestModelWithTaus/mstop_500__xqcut_80__qcut_150__light_lep   

echo "copying root files to work space"
cp *root /afs/cern.ch/user/b/bjackson/work/public/BMinusLSUSY_Generation/BMinusLSUSY/TestModelWithTaus/d3pd
