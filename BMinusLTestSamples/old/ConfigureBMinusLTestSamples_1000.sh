import model mssm
define p = g u c d s b u~ c~ d~ s~ b~
define j = p
generate p p > t1 t1~
add process p p > t1 t1~ j
output BMinusLTestSamples_1000
exit
