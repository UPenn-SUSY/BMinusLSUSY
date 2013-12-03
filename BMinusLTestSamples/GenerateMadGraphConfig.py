#!/usr/bin/env python

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
        add_process_line = '%s j' % add_process_line
        f.write("%s\n" % add_process_line)
        nj += 1
    f.write("\n")

    f.write("output %s\n" % model_name)
    f.write("exit\n")

    f.close()


generateConfig('test_100_nj0', 0)
generateConfig('test_100_nj1', 1)
generateConfig('test_100_nj2', 2)
generateConfig('test_100_nj3', 3)
