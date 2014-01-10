#!/bin/bash

source ~/.bash_profile

echo ""
echo "--------------------------------------------------------------------------------"
echo "Copying files to worker node"
cp -rf /afs/cern.ch/user/b/bjackson/work/public/BMinusLSUSY_Generation/BMinusLSUSY/TestModelWithTaus/../MadGraph5_v1_5_13 .
cp /afs/cern.ch/user/b/bjackson/work/public/BMinusLSUSY_Generation/BMinusLSUSY/TestModelWithTaus/mstop_500__xqcut_80__qcut_150__light_lep/CreateCard.py .
cp /afs/cern.ch/user/b/bjackson/work/public/BMinusLSUSY_Generation/BMinusLSUSY/TestModelWithTaus/mstop_500__xqcut_80__qcut_150__light_lep/Reference*Card.dat .

cp /afs/cern.ch/user/b/bjackson/work/public/BMinusLSUSY_Generation/BMinusLSUSY/TestModelWithTaus/LheToPool.sh .
cp /afs/cern.ch/user/b/bjackson/work/public/BMinusLSUSY_Generation/BMinusLSUSY/TestModelWithTaus/PoolToTruthNtup.sh .

echo ""
echo "--------------------------------------------------------------------------------"
echo "Running MadGraph"
cd MadGraph5_v1_5_13
/afs/cern.ch/user/b/bjackson/work/public/BMinusLSUSY_Generation/BMinusLSUSY/TestModelWithTaus/RunTestProduction.sh /afs/cern.ch/user/b/bjackson/work/public/BMinusLSUSY_Generation/BMinusLSUSY/TestModelWithTaus/mstop_500__xqcut_80__qcut_150__light_lep 500 80 150
cd ..

echo ""
echo "--------------------------------------------------------------------------------"
echo "Setting up Athena :-("
source /afs/cern.ch/user/b/bjackson/work/public/BMinusLSUSY_Generation/BMinusLSUSY/SetupAthena
echo "Done setting up Athena :-)"

echo ""
echo "--------------------------------------------------------------------------------"
echo "Converting LHE file(MadGraph5_v1_5_13/mstop_500__xqcut_80__qcut_150__light_lep/Events/unweighted_events.lhe) to pool file"
ls MadGraph5_v1_5_13/mstop_500__xqcut_80__qcut_150__light_lep/Events/unweighted_events.lhe
.//LheToPool.sh MadGraph5_v1_5_13/mstop_500__xqcut_80__qcut_150__light_lep/Events/unweighted_events.lhe mstop_500__xqcut_80__qcut_150__light_lep
ls

echo ""
echo "--------------------------------------------------------------------------------"
echo "Converting Pool file to truth ntuple"
.//PoolToTruthNtup.sh mstop_500__xqcut_80__qcut_150__light_lep
ls

echo ""
echo "--------------------------------------------------------------------------------"
echo "copying root files to work space"
cp *root /afs/cern.ch/user/b/bjackson/work/public/BMinusLSUSY_Generation/BMinusLSUSY/TestModelWithTaus/d3pd

