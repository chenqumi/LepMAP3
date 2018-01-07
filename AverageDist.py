#chenqumi@20171109
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import sys,os,re

if len(sys.argv) ==1:
    print("\nUsage: {} <LG.map.lst>".format(sys.argv[0]))
    sys.exit()

lst = sys.argv[1]

output = open("averagedistance.stat","w")
with open(lst) as lst_fd:
    output.write("LG\tmarker_num\tmap_marker_num\tdistance\taverdist\n")
    for line in lst_fd:
        
        line = line.strip()
        file = os.path.basename(line)
        
        with open (file) as fd:
            
            dic = {}
            marker_num = 0
            distance = ""
            
            for i in fd:
                
                i = i.strip()
                if i.startswith("#"):
                    lg = i.split("\t")[0].split("=")[1]
                    continue
                
                marker,pos = i.split("\t")
                dic[pos] = dic.get(pos,0) + 1
                distance = pos
                marker_num += 1

            map_marker_num = len(dic.keys())
            averdist = float(distance)/map_marker_num
            output.write("{}\t{}\t{}\t{}\t{}\n".format(lg,marker_num,map_marker_num,distance,averdist))

output.close()
