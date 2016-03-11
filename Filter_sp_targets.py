#!/usr/bin/env python

import sys

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SwissProt as sp

'''
This species_filter method takes four input arguments: (1) a uniprot-swissProt 
file handle, (2) a taxonomy id, (3) an output file handle, and (4) the set of 
EXP codes. If the function finds a protein that does NOT have any EXP evidence 
code, it writes the protein sequence for that protein to the output file.
'''

def species_filter(fh_sprot, taxon_id, fh_targets, EXP_default=set([])):
    target_id = int(taxon_id+"0000001")
    outseq_list = []
    seqCount = 0
    seqCount_exp = 0 
    for rec in sp.parse(fh_sprot):
        if taxon_id in rec.taxonomy_id: # SELECTS records that are related to a specific taxon_id such as 559292 for yeast
            exp_code = 0 
            seqCount += 1
            for crossRef in rec.cross_references: # Going over the list of GO information
                if crossRef[0] == 'GO': # consider the cross_reference entries that relate to GO DB
                    goList = [crossRef[1], (crossRef[3].split(':'))[0], crossRef[2][0]]
                    if (crossRef[3].split(':'))[0] in EXP_default:
                        exp_code = 1
                        break
            if not exp_code: # if the protein does not have any experimental validation, then write out the sequence
                outseq = SeqRecord(Seq(rec.sequence),
                       id="T"+str(target_id),
                       description = "%s" %
                       (rec.entry_name))
                outseq_list = [outseq]
                SeqIO.write(outseq_list,fh_targets, "fasta")
                target_id += 1
                seqCount_exp += 1
    return (seqCount, seqCount_exp)

def species_filter_count(fh_sprot, taxon_id, EXP_default=set([])):
    seqCount = 0
    seqCount_exp = 0 
    for rec in sp.parse(fh_sprot):
        if taxon_id in rec.taxonomy_id: # SELECTS records that are related to a specific taxon_id such as 559292 for yeast
            exp_code = 0 
            seqCount += 1
            for crossRef in rec.cross_references: # Going over the list of GO information
                if crossRef[0] == 'GO': # consider the cross_reference entries that relate to GO DB
                    goList = [crossRef[1], (crossRef[3].split(':'))[0], crossRef[2][0]]
                    if (crossRef[3].split(':'))[0] in EXP_default:
                        exp_code = 1
                        break
            if not exp_code: # if the protein does not have any experimental validation, increase seqCount_exp 
                seqCount_exp += 1
    return (seqCount, seqCount_exp)

if __name__ == '__main__':
    print 'This program does not run independently'
    sys.exit(1)
     
