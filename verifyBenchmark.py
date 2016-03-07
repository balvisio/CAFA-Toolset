#!/usr/bin/env python
from collections import defaultdict
import sys
import os.path

'''
   This script verifies the Limited-Knowledge(LK) and No-Knowledge(NK) benchmark sets created by CreateBenchmark program.
'''

def verify_LK_benchmark(t1_iea, t1_exp, t2_exp, output_filename_LK_bpo,output_filename_LK_cco, output_filename_LK_mfo):
    # Initialize dictionaries for <protein, GOid> tuples from the three files t1_iea, t1_exp, t2_exp
    t1_dict_iea = defaultdict(lambda:set())

    t1_dict_mfo = defaultdict(lambda:set())
    t1_dict_bpo = defaultdict(lambda:set())
    t1_dict_cco = defaultdict(lambda:set())

    t2_dict_mfo = defaultdict(lambda:set())
    t2_dict_bpo = defaultdict(lambda:set())
    t2_dict_cco = defaultdict(lambda:set())

# Create dictionaries with <protein, GO terms> as <key, values> pairs from the entries with NOn-Experimental Evidence at time t1
    t1_iea_handle = open(t1_iea, 'r')
    for lines in t1_iea_handle: 
        cols = lines.strip().split('\t')
        if len(cols) < 15:
            continue
        t1_dict_iea[cols[1]].add(cols[4]) # column 1: protein name, column 2: GO term to depict the function of that protein
    t1_iea_handle.close()

# Create dictionaries with <protein, GO terms> as <key, values> pairs from the entries with Non-Experimental Evidence at time t1
    t1_exp_handle = open(t1_exp, 'r')
    for lines in t1_exp_handle:
        cols = lines.strip().split('\t')
        if len(cols) < 15:
            continue
        if cols[8] == 'F': # column 8: Ontology group
            t1_dict_mfo[cols[1]].add(cols[4]) # column 1: protein name, column 2: GO term to depict the function of that protein
        elif cols[8] == 'P':
            t1_dict_bpo[cols[1]].add(cols[4])
        elif cols[8] == 'C':
            t1_dict_cco[cols[1]].add(cols[4])
    t1_exp_handle.close()

# create dictionaries with <protein, GO terms> as <key, values> pairs from the entries with Experimental Evidence at time t2
    t2_handle = open(t2_exp, 'r')
    for lines in t2_handle:
        cols = lines.strip().split('\t')
        if len(cols) < 15:
            continue
        if cols[8] == 'F':
            t2_dict_mfo[cols[1]].add(cols[4])
        elif cols[8] == 'P':
            t2_dict_bpo[cols[1]].add(cols[4])
        elif cols[8] == 'C':
            t2_dict_cco[cols[1]].add(cols[4])
    t2_handle.close()
   
    LKcount = 0
    # Verify the benchmark entries in the benchmark file: output_filename_LK_bpo
    if os.path.exists(output_filename_LK_bpo) and os.stat(output_filename_LK_bpo).st_size != 0:
        outfile_LK_bpo_handle = open(output_filename_LK_bpo, 'r')
        for lines in outfile_LK_bpo_handle: 
            cols = lines.strip().split('\t')
            if cols[0] not in t1_dict_iea:
                print 'Error: an undesired protein ' + cols[0] + ' got selected in ' + output_filename_LK_bpo
                break
            elif cols[0] in t1_dict_bpo:
                print 'Error: selected protein ' + cols[0] + ' in ' + output_filename_LK_bpo + ' already had experimental evidence at t1'
                break
            elif cols[0] not in t2_dict_bpo or cols[1] not in t2_dict_bpo[cols[0]]:
                print 'Error: selected protein ' + cols[0] + ' in ' + output_filename_LK_bpo + ' has not gained experimental evidence at t2'
                break 
        outfile_LK_bpo_handle.close() 
        LKcount += 1

    # Verify the benchmark entries in the benchmark file: output_filename_LK_cco
    if os.path.exists(output_filename_LK_cco) and os.stat(output_filename_LK_cco).st_size != 0:
        outfile_LK_cco_handle = open(output_filename_LK_cco, 'r')
        for lines in outfile_LK_cco_handle:
            cols = lines.strip().split('\t')
            if cols[0] not in t1_dict_iea:
                print 'Error: an undesired protein ' + cols[0] + ' got selected in ' + output_filename_LK_cco
                break
            elif cols[0] in t1_dict_cco:
                print 'Error: selected protein ' + cols[0] + ' in ' + output_filename_LK_cco + ' already had experimental evidence at t1'
                break
            elif cols[0] not in t2_dict_cco or cols[1] not in t2_dict_cco[cols[0]]:
                print 'Error: selected protein ' + cols[0] + ' in ' + output_filename_LK_cco + ' has not gained experimental evidence at t2'
                break
        outfile_LK_cco_handle.close()
        LKcount += 1

    # Verify the benchmark entries in the benchmark file: output_filename_LK_mfo
    if os.path.exists(output_filename_LK_mfo) and os.stat(output_filename_LK_mfo).st_size != 0:
        outfile_LK_mfo_handle = open(output_filename_LK_mfo, 'r')
        for lines in outfile_LK_mfo_handle:
            cols = lines.strip().split('\t')
            if cols[0] not in t1_dict_iea:
                  print 'Error: an undesired protein ' + cols[0] + ' got selected in ' + output_filename_LK_mfo
                  break
            elif cols[0] in t1_dict_mfo:
                  print 'Error: selected protein ' + cols[0] + ' in ' + output_filename_LK_mfo + ' already had experimental evidence at t1'
                  break
            elif cols[0] not in t2_dict_mfo or cols[1] not in t2_dict_mfo[cols[0]]:
                  print 'Error: selected protein ' + cols[0] + ' in ' + output_filename_LK_mfo + ' has not gained experimental evidence at t2'
                  break
        outfile_LK_mfo_handle.close()
        LKcount += 1

    return LKcount

def verify_NK_benchmark(t1_iea, t1_exp, t2_exp, output_filename_NK_bpo, output_filename_NK_cco, output_filename_NK_mfo):
    t1_dict_iea = defaultdict(lambda:set())

    t1_dict_mfo = defaultdict(lambda:set())
    t1_dict_bpo = defaultdict(lambda:set())
    t1_dict_cco = defaultdict(lambda:set())

    t2_dict_mfo = defaultdict(lambda:set())
    t2_dict_bpo = defaultdict(lambda:set())
    t2_dict_cco = defaultdict(lambda:set())

# Create dictionaries with <protein, GO terms> as <key, values> pairs from the entries with NOn-Experimental Evidence at time t1
    t1_iea_handle = open(t1_iea, 'r')
    for lines in t1_iea_handle: 
        cols = lines.strip().split('\t')
        if len(cols) < 15:
            continue
        t1_dict_iea[cols[1]].add(cols[4]) # column 1: protein name, column 2: GO term to depict the function of that protein
    t1_iea_handle.close()

# Create dictionaries with <protein, GO terms> as <key, values> pairs from the entries with Non-Experimental Evidence at time t1
    t1_exp_handle = open(t1_exp, 'r')
    for lines in t1_exp_handle:
        cols = lines.strip().split('\t')
        if len(cols) < 15:
            continue
        if cols[8] == 'F': # column 8: Ontology group
            t1_dict_mfo[cols[1]].add(cols[4]) # column 1: protein name, column 2: GO term to depict the function of that protein
        elif cols[8] == 'P':
            t1_dict_bpo[cols[1]].add(cols[4])
        elif cols[8] == 'C':
            t1_dict_cco[cols[1]].add(cols[4])
    t1_exp_handle.close()

#Create dictionaries with <protein, GO terms> as <key, values> pairs from the entries with Experimental Evidence at time t2
    t2_handle = open(t2_exp, 'r')
    for lines in t2_handle:
        cols = lines.strip().split('\t')
        if len(cols) < 15:
            continue
        if cols[8] == 'F':
            t2_dict_mfo[cols[1]].add(cols[4])
        elif cols[8] == 'P':
            t2_dict_bpo[cols[1]].add(cols[4])
        elif cols[8] == 'C':
            t2_dict_cco[cols[1]].add(cols[4])
    t2_handle.close()

    NKcount = 0
    # Verify the benchmark entries in the benchmark file: output_filename_NK_bpo
    if os.path.exists(output_filename_NK_bpo) and os.stat(output_filename_NK_bpo).st_size != 0:
        outfile_NK_bpo_handle = open(output_filename_NK_bpo, 'r')
        for lines in outfile_NK_bpo_handle: 
            cols = lines.strip().split('\t')
            if cols[0] not in t1_dict_iea:
                print 'Error: an undesired protein ' + cols[0] + ' got selected in ' + output_filename_NK_bpo
                break
            elif cols[0] in t1_dict_bpo or cols[0] in t1_dict_cco or cols[0] in t1_dict_mfo:
                print 'Error: selected protein ' + cols[0] + ' in ' + output_filename_NK_bpo + ' already had experimental evidence at t1'
                break
            elif cols[0] not in t2_dict_bpo:
                print 'Error: selected protein ' + cols[0] + ' in ' + output_filename_NK_bpo + ' has not gained experimental evidence at t2'
                break 
        outfile_NK_bpo_handle.close() 
        NKcount += 1

    # Verify the benchmark entries in the benchmark file: output_filename_NK_cco
    if os.path.exists(output_filename_NK_cco) and os.stat(output_filename_NK_cco).st_size != 0:
        outfile_NK_cco_handle = open(output_filename_NK_cco, 'r')
        for lines in outfile_NK_cco_handle:
            cols = lines.strip().split('\t')
            if cols[0] not in t1_dict_iea:
                print 'Error: an undesired protein ' + cols[0] + ' got selected in ' + output_filename_NK_cco
                break
            elif cols[0] in t1_dict_bpo or cols[0] in t1_dict_cco or cols[0] in t1_dict_mfo:
                print 'Error: selected protein ' + cols[0] + ' in ' + output_filename_NK_cco + ' already had experimental evidence at t1'
                break
            elif cols[0] not in t2_dict_cco:
                print 'Error: selected protein ' + cols[0] + ' in ' + output_filename_NK_cco + ' has not gained experimental evidence at t2'
                break 
        outfile_NK_cco_handle.close() 
        NKcount += 1

    # Verify the benchmark entries in the benchmark file: output_filename_NK_mfo
    if os.path.exists(output_filename_NK_mfo) and os.stat(output_filename_NK_mfo).st_size != 0:
        outfile_NK_mfo_handle = open(output_filename_NK_mfo, 'r')
        for lines in outfile_NK_mfo_handle:
            cols = lines.strip().split('\t')
            if cols[0] not in t1_dict_iea:
                  print 'Error: an undesired protein ' + cols[0] + ' got selected in ' + output_filename_NK_mfo
                  break
            elif cols[0] in t1_dict_bpo or cols[0] in t1_dict_cco or cols[0] in t1_dict_mfo:
                  print 'Error: selected protein ' + cols[0] + ' in ' + output_filename_NK_mfo + ' already had experimental evidence at t1'
                  break
            elif cols[0] not in t2_dict_mfo:
                  print 'Error: selected protein ' + cols[0] + ' in ' + output_filename_NK_mfo + ' has not gained experimental evidence at t2'
                  break 
        outfile_NK_mfo_handle.close() 
        NKcount += 1

    return NKcount

if __name__ == "__main__":
    print 'This script does not run independently'
    sys.exit(1)

