#!/usr/bin/env python

'''
    This module has the following two methods:

    species_filter:
        This method takes four input arguments:
            (1) a uniprot-swissProt file handle,
            (2) a taxonomy id,
            (3) an output file handle for writing target sequences,
            (4) an output file handle for writing the mapping between
                target id and protein name, and
            (5) the set of EXP codes.
            
        If the function finds a protein that does NOT have any EXP evidence 
        code, it writes the protein sequence for that protein to the output 
        file. It also writes the mapping of target id and protein name to 
        the map file.

        It returns the following TWO values:
            Total number of sequences in the sprot file related to the the 
                taxonomy id
            Total number of sequences in the sprot file related to the the 
                taxonomy id whose annotations have EXP evidence

    species_filter_count:
        This method takes three arguments:
            (1) a uniprot-swissProt file handle
            (2) a taxonomy id
            (3) the set of EXP codes

        It returns TWO values:
            Total number of sequences in the sprot file related to the the 
                taxonomy id
            Total number of sequences in the sprot file related to the the 
                taxonomy id whose annotations have EXP evidence
'''
import sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SwissProt as sp

def species_filter(fh_sprot, taxon_id, fh_targets, 
                   fh_map, EXP_default=set([])):
    # Initializes the target_id:
    target_id = int(taxon_id+"0000001")
    outseq_list = []

    # Counts total number of sequences 
    # in the sprot file related to the the taxonomy id taxon_id:
    seqCount = 0

    # Counts total number of sequences in the sprot file related 
    # to the the taxonomy id taxon_id whose annotations have EXP 
    # evidence:
    seqCount_no_exp = 0

    for rec in sp.parse(fh_sprot):
        # Selects records that are related to a specific
        # taxonomy id taxon_id:
        if taxon_id in rec.taxonomy_id:
            exp_code = False 
            seqCount += 1
            # Going over the list of GO information:
            for crossRef in rec.cross_references: 
                # Consider the cross_reference entries 
                # that relate to GO DB:
                if crossRef[0] == 'GO':
                    goList = [crossRef[1], 
                             (crossRef[3].split(':'))[0], 
                             crossRef[2][0]]
                    if (crossRef[3].split(':'))[0] in EXP_default:
                        exp_code = True
                        break

            # If the protein has no EXP evidence,
            # write the sequence to the output file:
            if not exp_code:
#                outseq = SeqRecord(Seq(rec.sequence),
#                                   id="T"+str(target_id),
#                                   description = "%s" %
#                                   (rec.entry_name))

                outseq = SeqRecord(Seq(rec.sequence),
                                   id="T"+str(target_id),
                                   description = "%s\t%s" %
                                   (rec.entry_name, rec.accessions[0]))

#                outseq = SeqRecord(Seq(rec.sequence),
#                                   id="T"+str(target_id),
#                                   description = "%s" %
#                                   (rec.accessions[0]))
                outseq_list = [outseq]
                # Write out the sequence:
                SeqIO.write(outseq_list,fh_targets, "fasta")
                # Create target id -> protein name map string:
#                mapStr = "T" + str(target_id) + '\t' + \
#                               str(rec.entry_name) + '\n'

                mapStr = "T" + str(target_id) + '\t' + \
                               str(rec.entry_name) + '\t' + \
                               str(rec.accessions[0]) + '\n'

#                mapStr = "T" + str(target_id) + '\t' + \
#                               str(rec.accessions[0]) + '\n'

                # Write out the mapping (target id -> protein name):
                fh_map.write("%s" % mapStr)
                target_id += 1
                seqCount_no_exp += 1
#    return (seqCount, seqCount_no_exp)
    return seqCount_no_exp

def species_filter_count(fh_sprot, taxon_id, EXP_default=set([])):
    # The seqCopunt variable counts total number of sequences
    # in the sprot file related to the the taxonomy id taxon_id:
    seqCount = 0

    # The seqCount_exp variable counts total number of sequences in 
    # the sprot file related to the the taxonomy id taxon_id whose 
    # annotations have EXP evidence:
    seqCount_no_exp = 0
    
    # The rec_count counts the number of records
    rec_count = 0

    for rec in sp.parse(fh_sprot):
        rec_count += 1
        # SELECT records that are related to a specific
        # taxon_id such as 559292 for yeast:
        if taxon_id in rec.taxonomy_id:
            exp_code = False
            seqCount += 1
            # Go over the list of GO information:
            for crossRef in rec.cross_references:
                # Consider the cross_reference entries that 
                # relate to GO DB:
                if crossRef[0] == 'GO':
                    goList = [crossRef[1],
                              (crossRef[3].split(':'))[0], 
                              crossRef[2][0]]
                    if (crossRef[3].split(':'))[0] in EXP_default:
                        exp_code = True
                        break
            # If the protein has an no EXP evidence,
            # increase seqCount_no_exp:
            if not exp_code:
                seqCount_no_exp += 1
    return (rec_count, seqCount, seqCount_no_exp)

if __name__ == '__main__':
    print (sys.argv[0] + ':')
    print(__doc__)
    sys.exit(0)
