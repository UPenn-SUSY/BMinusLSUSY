#!/usr/bin/env python

import subprocess

mass_min = 100
# mass_max = 1000
mass_max = 200
mass_step = 100

# xqcut_min_factor = 10.
xqcut_min_factor = 5.
xqcut_max_factor = 2.
xqcut_step = 10

qcut_step = 10

counter = 0
for mass in xrange(mass_min, mass_max + mass_step, mass_step):
    xqcut_min = int(mass/xqcut_min_factor)
    xqcut_max = int(mass/xqcut_max_factor)
    print 'mass: %s  xqcut min: %s  xqcut max: %s' % (mass, xqcut_min, xqcut_max)
    for xqcut in xrange(xqcut_min, xqcut_max + xqcut_step, xqcut_step):
        qcut_min = xqcut + qcut_step
        qcut_max = xqcut*2
        for qcut in xrange(qcut_min, qcut_max + qcut_step, qcut_step):
            counter += 1

            print './SubmitToBatch.sh %s %s %s 8nh' % (mass, xqcut, qcut_step)
            sp = subprocess.Popen(['./SubmitToBatch.sh', '%s' % mass, '%s' % xqcut, '%s' % qcut, '8nh'], stdout=subprocess.PIPE)
            output = sp.communicate()

print counter
