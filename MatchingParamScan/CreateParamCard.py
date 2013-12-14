#!/usr/bin/env python

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
def produceParamCard(ref_param_card_name, output_param_card_name, replace_dict):
    param_card_lines = readRefParamCard(ref_param_card_name)

    for rd in replace_dict:
        print 'replacing %s with %s' % (rd, replace_dict[rd])
        replaceParam(param_card_lines, rd, replace_dict[rd])

    f = file(output_param_card_name, 'w')
    for pcl in param_card_lines:
        f.write(pcl)

# ------------------------------------------------------------------------------
def main():
    replace_dict = {'M_STOP': 500}

    produceParamCard('ReferenceParamCard.dat', 'TestParamCard.dat', replace_dict)

# ==============================================================================
if __name__ == '__main__':
    main()
