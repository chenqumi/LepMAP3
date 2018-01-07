#chenqumi@20171121
#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,re

if len(sys.argv) ==1:
    print("\nUsage: {} <orderfile.lst>".format(sys.argv[0]))
    sys.exit()

lst = sys.argv[1]

JAVA = "/lustre/project/og04/shichunwei/biosoft/jre1.8.0_91/bin/java"
LM = "/p299/user/og03/chenquan1609/Bin/LepMap3/bin"


with open(lst) as fd:
    for line in fd:
        line = line.strip()
        file = os.path.abspath(line)
        pattern = r".+/repeat(\d+)/order(\d+)\.txt"
        m = re.match(pattern,file)
        repeat = m.group(1)
        lg = m.group(2)
        cmd = "{} -Xmx30G -cp {} OrderMarkers2 ".format(JAVA,LM)
        cmd = cmd + "data=data.call evaluateOrder={} ".format(file)
        cmd = cmd + "improveOrder=0 outputPhasedData=1 sexAveraged=1 "
        cmd = cmd + "> lmplot{}_{}.txt &&".format(lg,repeat)

        cmd2 = "{} -cp {} LMPlot ".format(JAVA,LM)
        cmd2 = cmd2 + "lmplot{0}_{1}.txt > lmplot{0}_{1}.dot".format(lg,repeat)

        outfile = "lmplot_lg{}_{}.sh".format(lg,repeat)
        ot = open(outfile,"w")
        ot.write(cmd+"\n")
        ot.write(cmd2+"\n")
        ot.close()


