#chenqumi@20171012
#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,re
#import collections

if len(sys.argv) ==1:
    print("\nUsage: {} <map.txt>".format(sys.argv[0]))
    sys.exit()

mapfile = sys.argv[1]

#count = collections.OrderedDict()
count ={}
with open(mapfile) as fd:
    for line in fd:
        line = line.strip()
        if line.startswith("#"):
            continue
        grp = line.split()[0]
        count[grp] = count.get(grp,0) + 1    

dic_tmp = sorted(count.items(),key=lambda d:int(d[0]))


total_marker_num = 0

for item in dic_tmp:
    
    print ("LG{}:\t{}".format(item[0],item[1]))
    
    if item[0] != "0":
        total_marker_num += item[1]

print ("Total mapped marker:\t{}".format(total_marker_num))