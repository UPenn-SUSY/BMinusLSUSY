from MadGraphControl.MadGraphUtils import *
# ==============================================================================
# = stop pair-production with stop > b l
# ==============================================================================

# ------------------------------------------------------------------------------
# basic config stuff
print '--------------------------------------------------------------------------------'
print 'Setting basic config stuff'
print '--------------------------------------------------------------------------------'
therun = runArgs.runNumber-202632
if therun < 0 and therun >= 20:
    evgenLog.fatal('Invalid run number! Will fail now!')
    raise RuntimeError('Unknown run number')

masses = {}
masses['1000006'] = 50*therun+100 # 50 GeV scan over stop masses, 20 points
stringy = str(masses['1000006']) # Goes into the file name
gentype='TT' # stop-stop
decaytype='directBL' # your magic word
njets=0 # Number of jets in MadGraph
evgenLog.info('Registered generation of stop pair production, stop to bl; grid point '+str(therun)+' decoded into mass ' + str(masses['1000006']) + ', with ' + str(njets) + ' jets.')
use_decays=False # To turn on decays in MadGraph
evt_multiplier = 20.0

evgenConfig.contact  = [ "bjackson@cern.ch" ]
evgenConfig.keywords += ['stop']
evgenConfig.description = 'stop direct pair production with simplified model'
evgenConfig.minevents=50000

# ------------------------------------------------------------------------------
# Basic settings for production and filters
print '--------------------------------------------------------------------------------'
print 'Setting basic settings'
print '--------------------------------------------------------------------------------'
SLHAonly = False
syst_mod=None
use_Tauola=True
use_METfilter=False
use_MultiElecMuTauFilter=False
use_MultiLeptonFilter=False

# ------------------------------------------------------------------------------
# Set up skip events - should almost never be used
skip_events=0

# ------------------------------------------------------------------------------
# Set random seed
rand_seed=1234
if hasattr(runArgs, "randomSeed"):
    rand_seed=runArgs.randomSeed

# ------------------------------------------------------------------------------
# Set beam energy - default to 8 TeV c.o.m.
beamEnergy = 4000.
if hasattr(runArgs,'ecmEnergy'):
    beamEnergy = runArgs.ecmEnergy / 2.

# ------------------------------------------------------------------------------
if 'EventMultiplier' in dir(): evt_multiplier=EventMultiplier
if hasattr(runArgs,'EventMultiplier'): evt_multiplier=runArgs.EventMultiplier
nevts=5000*evt_multiplier
evt_multiplier=-1

# ------------------------------------------------------------------------------
# Set pythia6 or pythia8
usePythia6 = True

# ------------------------------------------------------------------------------
# Default matching parameters
print '--------------------------------------------------------------------------------'
print 'Finding matching parameters'
print '--------------------------------------------------------------------------------'
ickkw = 1
xqcut = masses['1000006']/4
qcut = xqcut
# xqcut = masses['1000006']/6
# while not xqcut%5 == 0:
#     xqcut -= 1
# qcut = 2*xqcut
print 'xqcut: %s' % xqcut
print 'qcut: %s' % qcut

# ------------------------------------------------------------------------------
# Write proc_card
print '--------------------------------------------------------------------------------'
print 'Writing proc_card'
print '--------------------------------------------------------------------------------'
proc_card_out = open('proc_card_mg5.dat','w')
proc_card_out.write("""
import model ReducedUFO
# Define multiparticle labels
define p = g u c d s u~ c~ d~ s~
define j = g u c d s u~ c~ d~ s~
define l+ = e+ mu+ ta+
define l- = e- mu- ta-
define vl = ve vm vt
# define vl~ = ve~ vm~ vt~
# define fu = u c e+ mu+ ta+
# define fu~ = u~ c~ e- mu- ta-
# define fd = d s ve~ vm~ vt~
# define fd~ = d~ s~ ve vm vt

# Specify process(es) to run

""")

starter = 'generate'
for jet_it in xrange(njets + 1):
    jet_string = ''
    for i in xrange(jet_it):
        jet_string += 'j '

    # proc_string = '%s p p > t1 t1~ %s $ go ul ur dl dr cl cr sl sr t2 b1 b2 ul~ ur~ dl~ dr~ cl~ cr~ sl~ sr~ b1~ t2~ b2~ @%d\n '% (starter, jet_string, jet_it)
    proc_string = '%s p p > t1 t1~ %s , t1 > b l+ , t1~ > b~ l- $ go ul ur dl dr cl cr sl sr t2 b1 b2 ul~ ur~ dl~ dr~ cl~ cr~ sl~ sr~ b1~ t2~ b2~ @%d\n '% (starter, jet_string, jet_it)

    proc_card_out.write(proc_string)

    starter = 'add process'

proc_card_out.write("""

# Output processes to MadEvent directory
output -f
""")
proc_card_out.close()
print 'Proc card is written and closed!'

# ------------------------------------------------------------------------------
# write run card
print '--------------------------------------------------------------------------------'
print 'Writing run_card'
print '--------------------------------------------------------------------------------'
alpsfact = 1.0
scalefact=1.0
build_run_card( run_card_old='run_card.SM.dat'
              , run_card_new='run_card.dat'
              , xqcut=xqcut
              , nevts=nevts
              , rand_seed=rand_seed
              , beamEnergy=beamEnergy
              , scalefact=scalefact
              , alpsfact=alpsfact
              )
print 'Done writing run_card'

# ------------------------------------------------------------------------------
# Write param_card
print '--------------------------------------------------------------------------------'
print 'Writing param_card'
print '--------------------------------------------------------------------------------'
offshellness = ''
decays = {}
dummy_param_card_name = 'param_card.SM.%s.%s.%sdat' % ( gentype
                                                      , decaytype
                                                      , offshellness
                                                      )
build_param_card( param_card_old=dummy_param_card_name
                , param_card_new='param_card.dat'
                , masses=masses
                , decays=decays
                )
print 'Done writing param_card'
print 'dummy param card: %s' % dummy_param_card_name
print 'new param_card: param_card.dat'

# ------------------------------------------------------------------------------
# generate process
print '--------------------------------------------------------------------------------'
print 'Creating new process'
print '--------------------------------------------------------------------------------'
process_dir = new_process()
# process_dir = 'PROC_mssm_0'
print 'prcess_dir: %s' % process_dir
# proc_card_out = open('proc_card_mg5.dat','w')

print 'Generating process'
generate( run_card_loc = 'run_card.dat'
        # , param_card_loc = None
        , param_card_loc = 'param_card.dat'
        , mode = 0
        , njobs = 1
        , run_name = 'Test'
        , proc_dir = process_dir
        )
print 'done generating process'

# if hasattr(runArgs,'skipEvents'):
#     skip_events = runArgs.skipEvents
# arrange_output( run_name = 'Test'
#               , proc_dir = process_dir
#               , outputDS = stringy + '._00001.events.tar.gz'
#               , skip_events = skip_events
#               )

# Move output files into the appropriate place, with the appropriate name
run_number = runArgs.runNumber
outputDS = 'madgraph.%i.madgraph_SM_%s_%s_%s._00001.events.tar.gz'%( run_number
                                                                   , gentype
                                                                   , decaytype
                                                                   , stringy
                                                                   )
print '--------------------------------------------------------------------------------'
print 'About to arrange output'
print '--------------------------------------------------------------------------------'
if arrange_output( run_name='Test'
                 , proc_dir=process_dir
                 , outputDS=outputDS
                 , skip_events=skip_events
                 ):
    mglog.error('Error arranging output dataset!')
    # return -1
    raise RuntimeError('Error arranging output dataset!')

# if not keepOutput:
#     mglog.info('Removing process directory...')
#     shutil.rmtree(thedir,ignore_errors=True)

# mglog.info('All done generating events!!')
# mglog.info('returning 2*xqcut as qcut value: %s' % 2*xqcut)
# return [2*xqcut,'madgraph.%i.madgraph_SM_%s_%s_%s._00001.events.tar.gz'%(run_number,gentype,decaytype,stringy)]


# ------------------------------------------------------------------------------
# Run pythia
print '--------------------------------------------------------------------------------'
print 'About to run pythia'
print '--------------------------------------------------------------------------------'
runArgs.qcut = qcut
runArgs.inputGeneratorFile = outputDS
if 'syst_mod' in dir():
    runArgs.syst_mod = syst_mod
runArgs.decaytype = decaytype
runArgs.gentype = gentype
runArgs.use_Tauola = use_Tauola
runArgs.use_METfilter = use_METfilter
runArgs.use_MultiElecMuTauFilter = use_MultiElecMuTauFilter
runArgs.use_MultiLeptonFilter = use_MultiLeptonFilter

if usePythia6:
    print 'running pythia6'
    evgenLog.info('Will use Pythia6...')
    include( 'MC12JobOptions/MadGraphControl_SimplifiedModelPythia6.py' )
else:
    print 'running pythia8'
    evgenLog.info('Will use Pythia8...')
    if 'mmjj' in dir(): runArgs.mmjj=mmjj
    if 'drjj' in dir(): runArgs.drjj=drjj
    if 'ptj'  in dir(): runArgs.ptj =ptj
    include( 'MC12JobOptions/MadGraphControl_SimplifiedModelPythia8.py' )
