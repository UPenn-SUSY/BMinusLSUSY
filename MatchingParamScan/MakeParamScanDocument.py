#!/usr/bin/env python

import os
import RemoveLegend as rl

import subprocess

# ------------------------------------------------------------------------------
def getAllSamples():
    sample_list = []
    for dirname, dirnames, filenames in os.walk('.'):
        if "mstop_" not in dirname:
            continue
        if "matching_plots" not in dirname:
            continue

        print '============================================================'
        print dirname

        splits = dirname.split('/')[1].split('__')
        print splits

        stop_mass = splits[0].split('_')[1]
        xqcut     = splits[1].split('_')[1]
        qcut      = splits[2].split('_')[1]

        # if not os.path.isfile('%s/DJR1.jpg' % dirname) or not os.path.isfile('%s/DJR2.jpg' % dirname):
        if not os.path.isfile('%s/DJR1.jpg' % dirname):
            continue

        # if int(xqcut) > 200:
        #     continue

        print 'stop_mass: %s' % stop_mass
        print 'xqcut    : %s' % xqcut
        print 'qcut     : %s' % qcut

        sample_list.append({'mass':stop_mass, 'xqcut':xqcut, 'qcut':qcut})

    return sample_list

# ------------------------------------------------------------------------------
def getFinalSamples():
    sample_list = []
    for stop_mass in xrange(100, 1100, 100):
        for modulus in [1, 5, 10]:
            xqcut = int(stop_mass / 6)
            while xqcut % modulus != 0:
                print '\txqcut(%s) mod %s != 0 -- decrementing by 1' % (xqcut, modulus)
                xqcut -= 1
            qcut = 2*xqcut

            print 'stop_mass: %s' % stop_mass
            print 'xqcut    : %s' % xqcut
            print 'qcut     : %s' % qcut

            dict_to_append = {'mass':stop_mass, 'xqcut':xqcut, 'qcut':qcut}
            if dict_to_append in sample_list:
                print '%s is already found in the sample list -- skipping' % dict_to_append
                continue

            # sample_list.append({'mass':stop_mass, 'xqcut':xqcut, 'qcut':qcut})
            sample_list.append(dict_to_append)

    print ''
    return sample_list

# ------------------------------------------------------------------------------
def orderSampleList(sample_list):
    return sorted(sample_list, key = lambda sl: 1e6*int(sl['mass']) + 1e3*int(sl['xqcut']) + int(sl['qcut']))

# ------------------------------------------------------------------------------
def preparePlots(sample_list):
    for sl in sample_list:
        print 'preparing plots for mstop=%s xqcut=%s qcut=%s' % (sl['mass'], sl['xqcut'], sl['qcut'])
        sample_dir_name = 'mstop_%s__xqcut_%s__qcut_%s' % (sl['mass'], sl['xqcut'], sl['qcut'])
        plot_dir_name = "%s/matching_plots" % sample_dir_name
        djr1 = "%s/DJR1" % plot_dir_name
        if not os.path.exists('%s.ps' % djr1):
            print '\tERROR: Missing matching plot: %s.ps' % djr1
            continue
        rl.removeLegend('%s.ps' % djr1, '%s_no_leg.ps' % djr1)

        sp1 = subprocess.Popen(['ps2epsi', '%s.ps' % djr1, '%s.epsi' % djr1], stdout=subprocess.PIPE)
        output = sp1.communicate()

        sp2 = subprocess.Popen(['ps2epsi', '%s_no_leg.ps' % djr1, '%s_no_leg.epsi' % djr1], stdout=subprocess.PIPE)
        output = sp2.communicate()

    print ''

# ------------------------------------------------------------------------------
def printLatexHeader(out_file):
    out_file.write("""\\documentclass[10pt]{article}
\\usepackage[margin=2cm]{geometry}
\\geometry{a4paper}
\\usepackage{graphicx}
\\usepackage{placeins}
\\DeclareGraphicsRule{.tif}{png}{.png}{`convert #1 `dirname #1`/`basename #1 .tif`.png}
\\usepackage{epstopdf}
% \\epstopdfsetup{update} % only regenerate pdf files when eps file is newer

\\title{MadGraph-Pythia matching plots}

\\begin{document}
\\maketitle

""")

# ------------------------------------------------------------------------------
def printMassHeading(out_file, stop_mass):
    out_file.write('\\FloatBarrier\n')
    out_file.write('\\newpage\n')
    out_file.write('\\section{Stop mass: %s}\n' % stop_mass)
    out_file.write('\n')
    out_file.write('\\FloatBarrier\n')
    out_file.write('\\newpage\n')

# ------------------------------------------------------------------------------
def printConfigPlots(out_file, sample_dict):
    print 'adding plots for sample_dict: %s' % sample_dict
    sample_dir_name = '../mstop_%s__xqcut_%s__qcut_%s' % (sample_dict['mass'], sample_dict['xqcut'], sample_dict['qcut'])
    plot_dir_name = "%s/matching_plots" % sample_dir_name
    # djr1_plot_name = "%s/DJR1.ps" % plot_dir_name
    # djr2_plot_name = "%s/DJR2.ps" % plot_dir_name
    djr1_plot_name = "%s/DJR1.epsi" % plot_dir_name
    djr1_no_leg_plot_name = "%s/DJR1_no_leg.epsi" % plot_dir_name
    # djr2_plot_name = "%s/DJR2.jpg" % plot_dir_name

    print 'dir_name: %s' % plot_dir_name
    print 'djr1: %s' % djr1_plot_name
    print 'djr1_no_leg: %s' % djr1_no_leg_plot_name
    # print 'djr2: %s' % djr2_plot_name
    print ''

    # out_file.write("mstop: %s\n" % sample_dict['mass'])
    # out_file.write('\\subsection{xqcut: %s :: qcut: %s}\n' % (sample_dict['xqcut'], sample_dict['qcut']))
    # out_file.write("%s\n" % djr1_plot_name)
    # out_file.write("%s\n" % djr2_plot_name)

    out_file.write("\\begin{figure}[h!]\n")
    out_file.write("\\centering\n")
    out_file.write("\\begin{minipage}{.5\\textwidth}\n")
    out_file.write("  \\centering\n")
    out_file.write("  \\includegraphics[width=\\linewidth]{%s}\n" % djr1_plot_name)
    # out_file.write("  \\caption{DJR1}\n")
    out_file.write("  DJR1\n")
    # out_file.write("  \\label{fig:test1}\n")
    out_file.write("\\end{minipage}%\n")
    out_file.write("\\begin{minipage}{.5\\textwidth}\n")
    out_file.write("  \\centering\n")
    # out_file.write("  \\includegraphics[width=\\linewidth]{%s}\n" % djr2_plot_name)
    out_file.write("  \\includegraphics[width=\\linewidth]{%s}\n" % djr1_no_leg_plot_name)
    # out_file.write("  \\caption{DJR2}\n")
    out_file.write("  DJR1 no legend\n")
    # out_file.write("  \label{fig:test2}\n")
    out_file.write("\\end{minipage}\n")
    out_file.write('\\caption{stop mass: %s :: xqcut: %s :: qcut: %s}\n' % (sample_dict['mass'], sample_dict['xqcut'], sample_dict['qcut']))
    out_file.write("\\end{figure}\n")
    out_file.write("\n")
    out_file.write('\\FloatBarrier\n')
    out_file.write("\n")

# ------------------------------------------------------------------------------
def printLatexFooter(out_file):
    out_file.write("""
\\end{document}
""")

# ------------------------------------------------------------------------------
def printLatexFile(out_dir, out_file_name, sample_list):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    f = file('%s/%s' % (out_dir, out_file_name), 'w')
    printLatexHeader(f)

    current_mass = None
    for sl in sample_list:
        if sl['mass'] != current_mass:
            printMassHeading(f, sl['mass'])
            current_mass = sl['mass']
        printConfigPlots(f, sl)

    printLatexFooter(f)

# ------------------------------------------------------------------------------
def main():
    # sample_list = getAllSamples()
    sample_list_final = getFinalSamples()

    # sample_list = orderSampleList(sample_list)
    sample_list_final = orderSampleList(sample_list_final)

    # preparePlots(sample_list)
    preparePlots(sample_list_final)

    # printLatexFile("MatchingPlotsDoc", "MatchingPlots.tex", sample_list)
    printLatexFile("MatchingPlotsFinalDoc", "MatchingPlotsFinal.tex", sample_list_final)

# ==============================================================================
if __name__ == '__main__':
    main()
