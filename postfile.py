#chenqumi@20170930
#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,re

if len(sys.argv) != 4:
    print("\nUsage: {} <vcf> <paternal ID> <maternal ID>".format(sys.argv[0]))
    sys.exit()

vcf,father,mother = sys.argv[1:4]

#
# ========================================
samples = []
with open (vcf) as fd:
    for line in fd:
        line = line.strip()
        if line.startswith("#CHROM"):
            samples = line.split("\t")[9:]
            break

sam_num = len(samples)
off_num = sam_num - 2
#
# ========================================

fam_tmp1 = ["F" for x in range(sam_num)]
fam_tmp2 = "\t".join(fam_tmp1)
fam = "CHR\tPOS\t{}".format(fam_tmp2)

index_m = samples.index(mother)
index_f = samples.index(father)
    
index_min = min(index_m,index_f)
index_max = max(index_m,index_f)
    
samples.pop(index_max)
samples.pop(index_min)
    
samples.insert(0,mother)
samples.insert(0,father)
samples.insert(0,"POS")
samples.insert(0,"CHR")
    
sample_id = "\t".join(samples)
#
# ========================================

father_tmp1 = [father for x in range(off_num)]
father_tmp2 = "\t".join(father_tmp1)
father_line = "CHR\tPOS\t0\t0\t{}".format(father_tmp2)
#
# ========================================

mother_tmp1 = [mother for x in range(off_num)]
mother_tmp2 = "\t".join(mother_tmp1)
mother_line = "CHR\tPOS\t0\t0\t{}".format(mother_tmp2)
#
# ========================================

line5_tmp = "\t".join(["0" for x in range(off_num)])
line5 = "CHR\tPOS\t1\t2\t{}".format(line5_tmp)
#
# ========================================

line6_tmp = "\t".join(["0" for x in range(sam_num)])
line6 = "CHR\tPOS\t{}".format(line6_tmp)
#
# ========================================
print (fam)
print (sample_id)
print (father_line)
print (mother_line)
print (line5)
print (line6)