#!/usr/bin/env python

include("MC12JobOptions/Pythia8_AU2_MSTW2008LO_Common.py")
include("MC12JobOptions/Pythia8_MadGraph.py")
#include("MC12JobOptions/Pythia8_Photos.py")

## For debugging only: print out some Pythia config info
topAlg.Pythia8.Commands += [ "Init:showAllParticleData = on"
                           , "Next:numberShowLHA = 10"
                           , "Next:numberShowEvent = 10"
                           ]
evgenConfig.description = "testing lhe interface"
evgenConfig.keywords = ["test"]
evgenConfig.inputfilecheck = 'SampleProcess'

