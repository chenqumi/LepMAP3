#chenqumi@20171013
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from scipy import stats
import sys,os,re
import argparse

# Args parse
#======================================
parser = argparse.ArgumentParser(description="Filter vcf for GeneticMap")

parser.add_argument("-v", dest="vcf", required=True,
                    help="input vcf file")

parser.add_argument("-f", dest="paternal", type=str, required=True,
                    help="paternal ID")

parser.add_argument("-m", dest="maternal", type=str, required=True,
                    help="maternal ID")

parser.add_argument("-d", dest="min_dp", type=int, default=5, 
                    help="permitted minimum DP [5]")

parser.add_argument("-r", dest="missing_rate", type=float, default=0.25, 
                    help="max-missing rate [0.25]")

parser.add_argument("-p", dest="P_threshold", type=float, default=0.001, 
                    help="pvalue threshold [0.001]")

args = parser.parse_args()
vcf = args.vcf
paternal = args.paternal
maternal = args.maternal
min_dp = args.min_dp
missing_rate = args.missing_rate
P_threshold = args.P_threshold

#
# ======================================
def parse_parent(maternal,paternal,line):
    
    samples = line.split("\t")
    index_m = samples.index(maternal)
    index_f = samples.index(paternal)
    
    index_min = min(index_m,index_f)
    index_max = max(index_m,index_f)
    
    samples.pop(index_max)
    samples.pop(index_min)
    
    samples.insert(9,maternal)
    samples.insert(9,paternal)
    
    sampleline = "\t".join(samples)

    return(index_m,index_f,index_min,index_max,sampleline)
    
#
# ======================================
def format_dp(sam):
    #dp = int(sam.split(":")[2])
    try:
        dp = sam.split(":")[2]
    except IndexError as e:
        dp = 0
        print (e)
    
    if dp == ".":
        dp = 0
    else: 
        dp = int(dp)
    #if dp <= min_dp:
    if dp < min_dp:
        sam = "./.:0,0:0:.:.:.:0,0,0"
    gt = sam.split(":")[0]
    return sam,gt

#
# =======================================
def segregation(gt_m,gt_f):
    gamete_m = gt_m.split("/")
    gamete_f = gt_f.split("/")
    ratio = {}
    for m in gamete_m:
        for f in gamete_f:
            zygote = "{}/{}".format(m,f)
            if zygote == "1/0":
                zygote = "0/1"
            ratio[zygote] = ratio.get(zygote,0) + 0.25
    return ratio

#
# ========================================
def check_offspring(gt_m,gt_f,off):
    ratio = segregation(gt_m,gt_f)
    if not ratio.get(off.split(":")[0]):
        off = "./.:0,0:0:.:.:.:0,0,0"
    off_gt = off.split(":")[0]

    return off,off_gt

#
# ========================================
def calc_exp(gt_m,gt_f,off_num):
    ratio = segregation(gt_m,gt_f)
    off_num = int(off_num)
    exp_00 = ratio.get("0/0",0)*off_num
    exp_01 = ratio.get("0/1",0)*off_num
    exp_11 = ratio.get("1/1",0)*off_num

    return exp_00,exp_01,exp_11
#
# ========================================

output = open("result.vcf","w")
with open(vcf) as fd:
    
    index_m = 0
    index_f = 0
    index_min = 0
    index_max = 0
    
    for line in fd:
        
        line = line.strip()
        if line.startswith("#"):
            if line.startswith("#CHROM"):
                
                (index_m,index_f,
                index_min,index_max,sampleline
                )=parse_parent(maternal,paternal,line)
                
                output.write(sampleline+"\n")
            else:
                output.write(line+"\n")
            continue
        
        lines = line.split("\t")
        tmp = lines[:9]
        
        mother = lines[index_m]
        father = lines[index_f]
        
        mother,gt_m = format_dp(mother)
        father,gt_f = format_dp(father)
        
        # filter Parent genotype
        if gt_m == "./.":
            continue
        elif gt_f == "./.":
            continue
        elif gt_m == "0/0" and gt_f == "0/0":
            continue
        elif gt_m == "1/1" and gt_f == "1/1":
            continue

        # set offspring as miss type
        count = {}
        
        offsprings_tmp1 = lines[9:index_min]
        offsprings_tmp2 = lines[index_min+1:index_max]
        offsprings_tmp3 = lines[index_max+1:]
        offsprings = offsprings_tmp1+offsprings_tmp2+offsprings_tmp3
        
        off_num = len(offsprings)
        sam_num = off_num + 2

        for off in offsprings:
            
            off,off_gt = format_dp(off)
            off,off_gt = check_offspring(gt_m,gt_f,off)
            
            tmp.append(off)
            count[off_gt] = count.get(off_gt,0) + 1

        num_00 = count.get("0/0",0)
        num_01 = count.get("0/1",0)
        num_11 = count.get("1/1",0)
        num_miss = count.get("./.",0)

        # filter max-missing
        if num_miss/off_num > missing_rate:
        #if num_miss/sam_num > missing_rate:
            continue

        # chi-square test
        effect_off_num = off_num - num_miss
        exp_00,exp_01,exp_11 = calc_exp(gt_m,gt_f,effect_off_num)

        obs_tmp = [num_00,num_01,num_11]
        exp_tmp = [exp_00,exp_01,exp_11]
        non_zero = [i for i in range(3) if exp_tmp[i] != 0]
        exp = [exp_tmp[i] for i in non_zero]
        obs = [obs_tmp[i] for i in non_zero]

        chi,pvalue = stats.chisquare(obs,f_exp=exp)
        
        if pvalue > P_threshold:
            tmp.insert(9,mother)
            tmp.insert(9,father)
            newline = "\t".join(tmp)
            output.write(newline+"\n")

output.close()
