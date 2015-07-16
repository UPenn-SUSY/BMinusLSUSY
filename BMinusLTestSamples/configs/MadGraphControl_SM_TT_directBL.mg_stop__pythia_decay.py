include ( 'MC15JobOptions/MadGraphControl_SimplifiedModelPreInclude.py' )

# ------------------------------------------------------------------------------
# basic config stuff
print '--------------------------------------------------------------------------------'
print 'Setting basic config stuff'
print '--------------------------------------------------------------------------------'
therun = runArgs.runNumber-202632
if therun < 0 and therun >= 50:
    evgenLog.fatal('Invalid run number! Will fail now!')
    raise RuntimeError('Unknown run number')
masses['1000006'] = 50*therun+100 # 50 GeV scan over stop masses, 20 points

gentype = 'TT'
decaytype='directBL' # your magic word
njets=0

process = ''
starter = 'generate'
for jet_it in xrange(njets+1):
    jet_string = ''
    for i in xrange(jet_it):
        jet_string += 'j '

    proc_string = '%s p p > t1 t1~ %s $ go susylq susylq~ b1 b2 t2 b1~ b2~ t2~ @%d' % (starter, jet_string, jet_it)
    process = '\n'.join([process, proc_string])
    # process = '%s%s\n' % (process, proc_string)

    starter = 'add process'

# evt_multiplier = 20.0
evt_multiplier = 1.0
evgenLog.info('Registered generation of stop pair production, stop to bl; grid point '+str(therun)+' decoded into mass ' + str(masses['1000006']) + ', with ' + str(njets) + ' jets.')

evgenConfig.contact  = [ "bjackson@cern.ch" ]
evgenConfig.keywords += ['stop']
evgenConfig.description = 'stop direct pair production with simplified model'

include ( 'MC15JobOptions/MadGraphControl_SimplifiedModelPostInclude.py' )

if njets>0:
    genSeq.Pythia8.Commands += ["Merging:Process = pp>{t1,1000006}{t1~,-1000006}"]
