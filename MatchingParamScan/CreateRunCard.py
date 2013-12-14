#*********************************************************************
#                       MadGraph/MadEvent                            *
#                  http://madgraph.hep.uiuc.edu                      *
#                                                                    *
#                        run_card.dat                                *
#                                                                    *
#  This file is used to set the parameters of the run.               *
#                                                                    *
#  Some notation/conventions:                                        *
#                                                                    *
#   Lines starting with a '# ' are info or comments                  *
#                                                                    *
#   mind the format:   value    = variable     ! comment             *
#*********************************************************************
#
#*******************                                                 
# Running parameters
#*******************                                                 
#                                                                    
#*********************************************************************
# Tag name for the run (one word)                                    *
#*********************************************************************
  'fermi'     = run_tag ! name of the run 
#*********************************************************************
# Run to generate the grid pack                                      *
#*********************************************************************
  .false.     = gridpack  !True = setting up the grid pack
#*********************************************************************
# Number of events and rnd seed                                      *
# Warning: Do not generate more than 100K event in a single run      *
#*********************************************************************
  100000       = nevents ! Number of unweighted events requested 
   1      = iseed   ! rnd seed (0=assigned automatically=default)) 
#*********************************************************************
# Collider type and energy                                           *
#*********************************************************************
        1     = lpp1  ! beam 1 type (0=NO PDF)
        1     = lpp2  ! beam 2 type (0=NO PDF)
   4000      = ebeam1  ! beam 1 energy in GeV 
   4000      = ebeam2  ! beam 2 energy in GeV 
#*********************************************************************
# Beam polarization from -100 (left-handed) to 100 (right-handed)    *
#*********************************************************************
        0     = polbeam1 ! beam polarization for beam 1
        0     = polbeam2 ! beam polarization for beam 2
#*********************************************************************
# PDF CHOICE: this automatically fixes also alpha_s and its evol.    *
#*********************************************************************
 'cteq6l1'    = pdlabel     ! PDF set                                     
#*********************************************************************
# Renormalization and factorization scales                           *
#*********************************************************************
 F        = fixed_ren_scale  ! if .true. use fixed ren scale
 F        = fixed_fac_scale  ! if .true. use fixed fac scale
 91.1880  = scale            ! fixed ren scale
 91.1880  = dsqrt_q2fact1    ! fixed fact scale for pdf1
 91.1880  = dsqrt_q2fact2    ! fixed fact scale for pdf2
 1.00     = scalefact        ! scale factor for event-by-event scales 
#*********************************************************************
# Matching - Warning! ickkw > 1 is still beta
#*********************************************************************
 1        = ickkw            ! 0 no matching, 1 MLM, 2 CKKW matching
 1        = highestmult      ! for ickkw=2, highest mult group
 1        = ktscheme         ! for ickkw=1, 1 Durham kT, 2 Pythia pTE
 1.00     = alpsfact         ! scale factor for QCD emission vx 
 F        = chcluster        ! cluster only according to channel diag
 T        = pdfwgt           ! for ickkw=1, perform pdf reweighting
#*********************************************************************
# (turn off for VBF and single top processes)
#**********************************************************
   T  = auto_ptj_mjj
#**********************************************************
#                                                                    
#**********************************
# BW cutoff (M+/-bwcutoff*Gamma)
#**********************************
  15  = bwcutoff
#**********************************************************
# Apply pt/E/eta/dr/mij cuts on decay products or not
# (note that etmiss/ptll/ptheavy/sorted cuts always apply)
#**********************************************************
   T  = cut_decays
#*************************************************************
# Number of helicities to sum per event (0 = all helicities)
# 0 gives more stable result, but longer run time (needed for
# long decay chains e.g.).
# Use >=2 if most helicities contribute, e.g. pure QCD.
#*************************************************************
   0  = nhel
#*******************                                                 
# Standard Cuts
#*******************                                                 
#                                                                    
#*********************************************************************
# Minimum and maximum pt's                                           *
#*********************************************************************
  0  = ptj       ! minimum pt for the jets 
  0  = ptb       ! minimum pt for the b 
 10  = pta       ! minimum pt for the photons 
 10  = ptl       ! minimum pt for the charged leptons 
  0  = misset    ! minimum missing Et (sum of neutrino's momenta)
  0  = ptheavy   ! minimum pt for one heavy final state
 1.0 = ptonium   ! minimum pt for the quarkonium states
 1d5 = ptjmax    ! maximum pt for the jets
 1d5 = ptbmax    ! maximum pt for the b
 1d5 = ptamax    ! maximum pt for the photons
 1d5 = ptlmax    ! maximum pt for the charged leptons
 1d5 = missetmax ! maximum missing Et (sum of neutrino's momenta)
#*********************************************************************
# Minimum and maximum E's (in the lab frame)                         *
#*********************************************************************
  0  = ej     ! minimum E for the jets 
  0  = eb     ! minimum E for the b 
  0  = ea     ! minimum E for the photons 
  0  = el     ! minimum E for the charged leptons 
 1d5  = ejmax ! maximum E for the jets
 1d5  = ebmax ! maximum E for the b
 1d5  = eamax ! maximum E for the photons
 1d5  = elmax ! maximum E for the charged leptons
#*********************************************************************
# Maximum and minimum rapidity                                       *
#*********************************************************************
   5  = etaj    ! max rap for the jets 
 1d2  = etab    ! max rap for the b 
 2.5  = etaa    ! max rap for the photons 
 2.5  = etal    ! max rap for the charged leptons 
 0.6  = etaonium ! max rap for the quarkonium states
 0d0  = etajmin ! min rap for the jets
 0d0  = etabmin ! min rap for the b
 0d0  = etaamin ! min rap for the photons
 0d0  = etalmin ! main rap for the charged leptons
#*********************************************************************
# Minimum and maximum DeltaR distance                                *
#*********************************************************************
 0   = drjj    ! min distance between jets 
 0   = drbb    ! min distance between b's 
 0.4 = drll    ! min distance between leptons 
 0.4 = draa    ! min distance between gammas 
 0   = drbj    ! min distance between b and jet 
 0.4 = draj    ! min distance between gamma and jet 
 0.4 = drjl    ! min distance between jet and lepton 
 0   = drab    ! min distance between gamma and b 
 0   = drbl    ! min distance between b and lepton 
 0.4 = dral    ! min distance between gamma and lepton 
 1d2 = drjjmax ! max distance between jets
 1d2 = drbbmax ! max distance between b's
 1d2 = drllmax ! max distance between leptons
 1d2 = draamax ! max distance between gammas
 1d2 = drbjmax ! max distance between b and jet
 1d2 = drajmax ! max distance between gamma and jet
 1d2 = drjlmax ! max distance between jet and lepton
 1d2 = drabmax ! max distance between gamma and b
 1d2 = drblmax ! max distance between b and lepton
 1d2 = dralmax ! maxdistance between gamma and lepton
#*********************************************************************
# Minimum and maximum invariant mass for pairs                       *
#*********************************************************************
 0   = mmjj    ! min invariant mass of a jet pair 
 0   = mmbb    ! min invariant mass of a b pair 
 0   = mmaa    ! min invariant mass of gamma gamma pair
 0   = mmll    ! min invariant mass of l+l- (same flavour) lepton pair
 1d5 = mmjjmax ! max invariant mass of a jet pair
 1d5 = mmbbmax ! max invariant mass of a b pair
 1d5 = mmaamax ! max invariant mass of gamma gamma pair
 1d5 = mmllmax ! max invariant mass of l+l- (same flavour) lepton pair
#*********************************************************************
# Minimum and maximum invariant mass for all letpons                 *
#*********************************************************************
 0   = mmnl    ! min invariant mass for all letpons (l+- and vl) 
 1d5 = mmnlmax ! max invariant mass for all letpons (l+- and vl) 
#*********************************************************************
# Minimum and maximum pt for 4-momenta sum of leptons                *
#*********************************************************************
 0   = ptllmin  ! Minimum pt for 4-momenta sum of leptons(l and vl)
 1d5 = ptllmax  ! Maximum pt for 4-momenta sum of leptons(l and vl)
#*********************************************************************
# Inclusive cuts                                                     *
#*********************************************************************
 0  = xptj ! minimum pt for at least one jet  
 0  = xptb ! minimum pt for at least one b 
 0  = xpta ! minimum pt for at least one photon 
 0  = xptl ! minimum pt for at least one charged lepton 
#*********************************************************************
# Control the pt's of the jets sorted by pt                          *
#*********************************************************************
 0   = ptj1min ! minimum pt for the leading jet in pt
 0   = ptj2min ! minimum pt for the second jet in pt
 0   = ptj3min ! minimum pt for the third jet in pt
 0   = ptj4min ! minimum pt for the fourth jet in pt
 1d5 = ptj1max ! maximum pt for the leading jet in pt 
 1d5 = ptj2max ! maximum pt for the second jet in pt
 1d5 = ptj3max ! maximum pt for the third jet in pt
 1d5 = ptj4max ! maximum pt for the fourth jet in pt
 0   = cutuse  ! reject event if fails any (0) / all (1) jet pt cuts
#*********************************************************************
# Control the Ht(k)=Sum of k leading jets                            *
#*********************************************************************
 0   = htjmin ! minimum jet HT=Sum(jet pt)
 1d5 = htjmax ! maximum jet HT=Sum(jet pt)
 0   = ihtmin  !inclusive Ht for all partons (including b)
 1d5 = ihtmax  !inclusive Ht for all partons (including b)
 0   = ht2min ! minimum Ht for the two leading jets
 0   = ht3min ! minimum Ht for the three leading jets
 0   = ht4min ! minimum Ht for the four leading jets
 1d5 = ht2max ! maximum Ht for the two leading jets
 1d5 = ht3max ! maximum Ht for the three leading jets
 1d5 = ht4max ! maximum Ht for the four leading jets
#*********************************************************************
# WBF cuts                                                           *
#*********************************************************************
 0   = xetamin ! minimum rapidity for two jets in the WBF case  
 0   = deltaeta ! minimum rapidity for two jets in the WBF case 
#*********************************************************************
# maximal pdg code for quark to be considered as a light jet         *
# (otherwise b cuts are applied)                                     *
#*********************************************************************
 4 = maxjetflavor
#*********************************************************************
# Jet measure cuts                                                   *
#*********************************************************************
25.000000   = xqcut   ! minimum kt jet measure between partons 
#*********************************************************************
#*********************************************************************
30 = ktdurham   ! minimum kt in ktdurham algorithm
0.4 = dparameter  ! D0 parameter for ktDurham
F = dokt    ! perform the ktDurham cut
#*********************************************************************
