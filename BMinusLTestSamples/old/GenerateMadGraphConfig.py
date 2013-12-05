#!/usr/bin/env python

import sys
import os.path
import optparse
import time

import argparse

def generateConfig(model_name, num_extra_jets=0):
    f = file('config_%s.sh' % model_name, "w")

    f.write("import model mssm\n")
    f.write("define p = g u c d s b u~ c~ d~ s~ b~\n")
    f.write("define j = p\n")
    f.write("\n")

    process_line = f.write("generate p p > t1 t1~\n")
    add_process_line = 'add process p p > t1 t1~'
    nj = 1
    while nj <= num_extra_jets:
        print 'nj: %d -- %d' % (nj, num_extra_jets)
        add_process_line = '%s j' % add_process_line
        f.write("%s\n" % add_process_line)
        nj += 1
    f.write("\n")

    f.write("output %s\n" % model_name)
    f.write("exit\n")

    f.close()

def main():
    print 'Generating MadGraph config file:'
    parser = argparse.ArgumentParser(description='Generate MadGraph config file.')
    parser.add_argument( '--model-dir', dest='model_dir', action='store'
                       , default=None
                       , help='model directory'
                       )
    parser.add_argument( '--stop-mass', dest='stop_mass', action='store'
                       , default=None, type=int
                       , help='stop mass'
                       )
    parser.add_argument( '--num-partons', dest='num_partons', action='store'
                       , default=None, type=int
                       , help='number additional partons'
                       )
    args = parser.parse_args()

    model_dir = args.model_dir
    stop_mass = args.stop_mass
    num_partons = args.num_partons

    if model_dir is None:
        model_dir = raw_input("Model dir: ")
    if stop_mass is None:
        stop_mass = int(raw_input("Stop mass: "))
    if num_partons is None:
        num_partons = int(raw_input("Number additional partons: "))

    model_name = '%s_%s_np%s' % (model_dir, stop_mass, num_partons)

    print 'model_dir: %s' % model_dir
    print 'stop_mass: %s' % stop_mass
    print 'num_partons: %s' % num_partons
    print 'model name: %s ' % model_name

    generateConfig(model_name, num_partons)

if __name__ == '__main__':
    main()
