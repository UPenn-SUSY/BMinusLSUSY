##################################
# Stop pair-production with stop > b l
include('MC12JobOptions/MadGraphControl_SimplifiedModelPreInclude.py' )

# Assigned run numbers later - 400k+ for now
therun = runArgs.runNumber-400000
if therun>=0 and therun<20:
    masses['1000006'] = 50*therun+100 # 50 GeV scan over stop masses, 20 points
    stringy = str(masses['1000006']) # Goes into the file name
    gentype='TT' # stop-stop
    decaytype='directBL' # your magic word
    njets=1 # Number of jets in MadGraph
    evgenLog.info('Registered generation of stop pair production, stop to bl; grid point '+str(therun)+' decoded into mass ' + str(masses['1000006']) + ', with ' + str(njets) + ' jets.')
    use_decays=False # To turn on decays in MadGraph
    evt_multiplier = 20.0

evgenConfig.contact  = [ "bjackson@cern.ch" ] # Didn't look to see if that's right ;-)
evgenConfig.keywords += ['stop']
evgenConfig.description = 'stop direct pair production with simplified model'

include ( 'MC12JobOptions/MadGraphControl_SimplifiedModelPostInclude.py' )
##################################

