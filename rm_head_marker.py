#chenqumi@20171121
#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,re

if len(sys.argv) != 3:
    print("\nUsage: {} <orderfile> <rm former marker num>".format(sys.argv[0]))
    sys.exit()

file,num = sys.argv[1:3]
num = int(num)

index = 0
init_m_pos = 0.00
init_f_pos = 0.00
with open(file) as fd:
    for line in fd:
        line = line.strip()
        if line.startswith("#"):
            print (line)
            continue
        
        index += 1
        
        if index <= num:
            continue
        
        marker,m_pos,f_pos,other = line.split("\t",3)
        m_pos = float(m_pos)
        f_pos = float(f_pos)

        if index == num + 1:
            init_m_pos = m_pos
            init_f_pos = f_pos

        new_m_pos = m_pos - init_m_pos
        new_f_pos = f_pos - init_f_pos
        info = "{}\t{:.2f}\t{:.2f}\t{}".format(marker,new_m_pos,new_f_pos,other)
        print (info)
        
