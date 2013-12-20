#!/usr/bin/env python

import sys
import os.path
import optparse
import time

# ------------------------------------------------------------------------------
def removeLegend(in_file, out_file):
    in_f = file(in_file)
    out_f = file(out_file, 'w')
    # lines = []
    remove_next = False
    for l in in_f.readlines():
        if 'gsave' in l:
            remove_next = False

        if 'Sum of contributions' in l:
            remove_next = True

        if 'jet sample' in l:
            remove_next = True

        if '[ 12 12]' in l:
            remove_next = True

        if not remove_next:
            out_f.write(l)

# ------------------------------------------------------------------------------
def main():
    in_file = sys.argv[1]
    out_file = sys.argv[2]

    removeLegend(in_file, out_file)

# ==============================================================================
if __name__ == '__main__':
    main()
