#!/usr/bin/env python

import os

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

        if not os.path.isfile('%s/DJR1.jpg' % dirname) or not os.path.isfile('%s/DJR2.jpg' % dirname):
            continue

        if xqcut > 200:
            continue

        print 'stop_mass: %s' % stop_mass
        print 'xqcut    : %s' % xqcut
        print 'qcut     : %s' % qcut

        sample_list.append({'mass':stop_mass, 'xqcut':xqcut, 'qcut':qcut})
    return sample_list

# ------------------------------------------------------------------------------
def printLatexHeader(out_file):
    out_file.write("""\\documentclass[10pt]{article}
\\usepackage[margin=2cm]{geometry}
\\geometry{a4paper}
\\usepackage{graphicx}
\\usepackage{placeins}
\\DeclareGraphicsRule{.tif}{png}{.png}{`convert #1 `dirname #1`/`basename #1 .tif`.png}

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
    djr1_plot_name = "%s/DJR1.jpg" % plot_dir_name
    djr2_plot_name = "%s/DJR2.jpg" % plot_dir_name

    print 'dir_name: %s' % plot_dir_name
    print 'djr1: %s' % djr1_plot_name
    print 'djr2: %s' % djr2_plot_name
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
    out_file.write("  \\includegraphics[width=\\linewidth]{%s}\n" % djr2_plot_name)
    # out_file.write("  \\caption{DJR2}\n")
    out_file.write("  DJR2\n")
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
    sample_list = getAllSamples()

    printLatexFile("MatchingPlotsDoc", "MatchingPlots.tex", sample_list)

# ==============================================================================
if __name__ == '__main__':
    main()
