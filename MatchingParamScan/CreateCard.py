#!/usr/bin/env python

import sys
import os.path
import optparse
import time

# ------------------------------------------------------------------------------
def readRefParamCard(ref_param_card_name):
    f = file(ref_param_card_name)

    param_card_lines = []

    for l in f.readlines():
        param_card_lines.append(l)

    return param_card_lines

# ------------------------------------------------------------------------------
def replaceParam(param_card_lines, param_to_replace, value):
    for i, l in enumerate(param_card_lines):
        if param_to_replace in l:
            param_card_lines[i] = l.replace(param_to_replace, str(value))

# ------------------------------------------------------------------------------
def produceCard(ref_param_card_name, output_param_card_name, replace_dict):
    param_card_lines = readRefParamCard(ref_param_card_name)

    for rd in replace_dict:
        print 'replacing %s with %s' % (rd, replace_dict[rd])
        replaceParam(param_card_lines, rd, replace_dict[rd])

    f = file(output_param_card_name, 'w')
    for pcl in param_card_lines:
        f.write(pcl)

# ------------------------------------------------------------------------------
def main():
    ref_card = sys.argv[1]
    final_card = sys.argv[2]
    token = sys.argv[3]
    replace = sys.argv[4]

    produceCard(ref_card, final_card, {token:replace})

    # replace_dict = {'M_STOP': 500}

    # produceCard('ReferenceParamCard.dat' , 'TestParamCard.dat' , {'M_STOP':500})
    # produceCard('ReferenceRunCard.dat'   , 'TestRunCard.dat'   , {'XQCUT':30})
    # produceCard('ReferencePythiaCard.dat', 'TestPythiaCard.dat', {'QCUT':45})

# ==============================================================================
if __name__ == '__main__':
    main()
