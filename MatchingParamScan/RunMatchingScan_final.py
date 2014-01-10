#!/usr/bin/env python

import os
import subprocess

mass_min = 100
mass_max = 1000
mass_step = 100

counter = 0
for mass in xrange(mass_min, mass_max + mass_step, mass_step):
    xqcut = mass/6
    qcut = xqcut*2

    print 'mass: %s xqcut: %s qcut: %s' % (mass, xqcut, qcut)

    if os.path.exists('mstop_%s__xqcut_%s__qcut_%s' % (mass, xqcut, qcut)):
        print 'found directory: mstop_%s__xqcut_%s__qcut_%s -- skipping' % (mass, xqcut, qcut)
        continue
    counter += 1
    print './SubmitToBatch.sh %s %s %s 8nh' % (mass, xqcut, qcut)
    sp = subprocess.Popen(['./SubmitToBatch.sh', '%s' % mass, '%s' % xqcut, '%s' % qcut, '1nh'], stdout=subprocess.PIPE)
    output = sp.communicate()

print counter
