#chenqumi@20171121
#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,re

if len(sys.argv) ==1:
    print("\nUsage: {} <dotfile.lst>".format(sys.argv[0]))
    sys.exit()

lst = sys.argv[1]

with open(lst) as lst_fd:
    for line in lst_fd:
        line = line.strip()
        file = os.path.abspath(line)

        with open(file) as fd:
            for i in fd:
                i = i.strip()
                pattern = r"(\d+)--(\d+)\[*"

                if not re.match(pattern,i):
                    continue
                else:
                    m = re.match(pattern,i)
                    s = int(m.group(1))
                    e = int(m.group(2))
                    
                    if abs(s-e) != 1:
                        print ("Bad map:",file)
                        break



