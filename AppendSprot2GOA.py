#!/usr/bin/env python

'''
    This program takes four inputs: (1) a uniprot-swissprot file, (2) a 
    uniprot-GOA file, (3) taxon id, and (4) an output file. The GO terms 
    in the UniProt-SwissProt file that are NOT in the unprot-GOA file for 
    the supplied taxon id, are merged together with the uniprot-GOA file i
    and written to the output file.

    The entry point of this module is appendSprot2goa() method which calls 
    other the methods defined in this module:

    appendSprot2goa(fh_sprot, goa_file_name, taxon_id, fh_merged_go): 
        fh_sport: It is a file handle to a UniProtKB/SwissProt file.
        goa_file_name: It is a file name of a UniProt-GOA file.
        taxon_id: It is a Taxonomy Id for an organism. 
        fh_merged_go: It is file handle to the output file which
            already has all records copied into from the 
            UniProt-GOA file named goa_file_name. 
        This method goes over the records in fh_sprot file, checks 
        whether that records are already in UniProt-GOA file 
        goa_file_name, and if it is not found there, the method
        coverts the UniProtKB/SwissProt record to a UniProt-GOA record 
        by invoking swissProt2GOA and appends it to the end of the output file. 

    swissProt2GOA(sprotRec, crossRef, fields=GOAParser.GAF20FIELDS):
        This method converts a UniProtKB/SwissProt record to a UniProt-GOA 
        record by calling other methods defined in this module. And, at 
       the end, it returns the newly formed method.

    The list of other methods defined in this module are: 
    assignSymbol(sprotRec)
    assignGO_REF(sprotRec, crossRef)
    assignDB_REF(sprotRec, crossRef)
    assignSynonym(sprotRec)
    assignTaxoId(sprotRec)
    assignDate(sprotRec)
    create_iterator(infile)
'''

import os
import sys
import subprocess
import math
import calendar
from datetime import datetime
from dateutil import relativedelta

from Bio import SwissProt as sp
import GOAParser
import GOAParser_cafa as gc

Months = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def assignSymbol(sprotRec): 
    symbol = '' 
# scenario 1: gene_name=> Name=DBP5; Synonyms=RAT8; OrderedLocusNames=YOR046C;
# scenario 2: gene_name=> Name=DCS2 {ECO:0000312|SGD:S000005699}; OrderedLocusNames=YOR173W; ORFNames=O3625;
# scenario 3: gene_name=> Name=DDI2; OrderedLocusNames=YFL061W;
    for g in sprotRec.gene_name.strip(';').split(';'):
        if not g or g.find('=') == -1:
            continue 
        for f in g.split('=')[1].split(','): # split each memmber of the group g to a list 
            symbol = ((f.split(' '))[0]).strip()
            break
        if not symbol and not symbol.isspace():# the symbol happens to be not found in the above group g
            continue
        else:
            break
    return symbol # symbol is extracted from gene_name field of sprotRec and then return

def assignGO_REF(sprotRec, crossRef):
    go_ref = ''
    return go_ref

def find_pubmed(sprotRec):
    for ro in sprotRec.references:
        for tp in ro.references:
            if len(tp) >= 2 and tp[0].upper() == 'PUBMED':
                return tp[1] 
    return None 

def find_doi(sprotRec):
    for ro in sprotRec.references:
        for tp in ro.references:
            if len(tp) >= 2 and tp[0].upper() == 'DOI':
                return tp[1] 
    return None 

def find_reactome_id(sprotRec):
    for tp in sprotRec.cross_references: 
        if len(tp)>=2 and tp[0].upper() == 'REACTOME':
            return tp[1]
    return None 

def assignDB_REF(sprotRec, crossRef):
    if (find_pubmed(sprotRec) is not None):
        return 'PMID' + ':' + find_pubmed(sprotRec)
    elif (find_doi(sprotRec) is not None):
        return 'DOI' + ':' + find_doi(sprotRec)
    elif (find_reactome_id(sprotRec) is not None):
        return 'Reactome' + ':' + find_reactome_id(sprotRec)
    else:
        return assignGO_REF(sprotRec, crossRef)
     
def assignSynonym(sprotRec):
    synonym = []
# scenario 1: entry_name=> DBP5_YEAST
# scenario 2: entry_name=> DCS2_YEAST
# scenario 3: entry_name=> DDI2_YEAST
    synonym.append(sprotRec.entry_name)
# scenario 1: gene_name=> Name=DBP5; Synonyms=RAT8; OrderedLocusNames=YOR046C;
# scenario 2: gene_name=> Name=DCS2 {ECO:0000312|SGD:S000005699}; OrderedLocusNames=YOR173W; ORFNames=O3625;
# scenario 3: gene_name=> Name=DDI2; OrderedLocusNames=YFL061W;
    for g in sprotRec.gene_name.strip(';').split(';'):
        if not g or g.find('=') == -1:
            continue 
        for f in g.split('=')[1].split(','): # split each memmber of the group g to a list
            tmpStr = ((f.split(' '))[0]).strip()
            if not tmpStr and not tmpStr.isspace():
                pass
            else:
                synonym.append(tmpStr)
    return synonym

def assignTaxoId(sprotRec):
    taxList = []
    for taxNo in sprotRec.taxonomy_id:
        taxList.append('taxon:' + taxNo)
    return taxList

def assignDate(sprotRec):
    date = ''
    yy_1=((sprotRec.created[0]).split('-'))[2]
    mm_1 = ((((sprotRec.created[0]).split('-'))[1]).title())
    dd_1 =((sprotRec.created[0]).split('-'))[0]
    yy_2=((sprotRec.annotation_update[0]).split('-'))[2]
    mm_2 = ((((sprotRec.annotation_update[0]).split('-'))[1]).title())
    dd_2 =((sprotRec.annotation_update[0]).split('-'))[0]
  
    if (datetime(int(yy_1), Months.index(mm_1),int(dd_1)) < datetime(int(yy_2), Months.index(mm_2), int(dd_2))):
        date = yy_2 + str(Months.index(mm_2)) + dd_2
    else:
        date = yy_1 + str(Months.index(mm_1)) + dd_1
    return date

def swissProt2GOA(sprotRec, crossRef, fields=GOAParser.GAF20FIELDS):
    """
     This method takes a SwissProt record and GO term information 
     as input arguments. It then constructs a GOA dictionary using 
     the 'fields' as keys and values taken from sprotReci, and then 
     returns the constructed GOA record.
    """
    # 15 fields are defined for GAF10FIELDS (GAF 1.0)
    goaRec = {'DB':'SwissProt', # 'SwissProt' is assigned to DB
              'DB_Object_ID': sprotRec.accessions[0],
              'DB_Object_Symbol': assignSymbol(sprotRec),
              'Qualifier': [], # is assinged an empty list
              'GO_ID': crossRef[1],
              'DB:Reference': assignDB_REF(sprotRec, crossRef),
              'Evidence': (crossRef[3].split(':'))[0],
              'With': [],
              'Aspect': (crossRef[2].split(':'))[0],
              'DB_Object_Name' : (crossRef[2].split(':'))[1],
              'Synonym': assignSynonym(sprotRec),
              'DB_Object_Type': 'protein',
              'Taxon_ID': assignTaxoId(sprotRec),
              'Date': assignDate(sprotRec),
              'Assigned_By': (crossRef[3].split(':'))[1]
              }
#    print goaRec['DB:Reference']

    if len(fields) == 17: # Two extra fields are defined for GAF20FIELDS (GAF 2.0)
        goaRec['Annotation_Extension'] = ''
        goaRec['Gene_Product_Form_ID'] = ''
    return goaRec

def create_iterator(infile):
    """
    It returns an iterator object for an input uniprot-goa file 
    along with a list of all fieldnames contained in the 
    uniprot-goa file.
    """ 
    infile_handle = open(infile, 'r')
    iter_handle = GOAParser.gafiterator(infile_handle)
    for ingen in iter_handle:
        if len(ingen) == 17:
            GAFFIELDS = GOAParser.GAF20FIELDS
            break
        else:
            GAFFIELDS = GOAParser.GAF10FIELDS
            break
    infile_handle.close()
    infile_handle = open(infile, 'r')
    iter_handle = GOAParser.gafiterator(infile_handle)
    return iter_handle, GAFFIELDS

def appendSprot2goa(fh_sprot, goa_file_name, taxon_id, fh_merged_go):
    """
     Append new GO terms from a uniPort-swisprot file 
     (file handle: fh_sprot) to SwissProt-GOA file (goa_file_name), 
     writing the merged file to a merged file (file handle: fh_merged_go)
    """
    # Creates an iterator object for t1 file:
    iter_handle, GAFFIELDS = create_iterator(goa_file_name) 

    # Construct a dictionary goa_dict with the proteins and 
    # the corresponding GO terms in t1 file:
    goa_dict = {}
    for ingen in iter_handle:
        if ingen['DB_Object_ID'] in goa_dict.keys():
            goa_dict[ingen['DB_Object_ID']].append([ingen['GO_ID'], ingen['Evidence'], ingen['Aspect']])
        else:
            goa_dict[ingen['DB_Object_ID']] = [[ingen['GO_ID'], ingen['Evidence'], ingen['Aspect']]]

# EXTRACTS the NEW GO terms in t2 file that are NOT found in t1 file
    goCount = 0
    for rec in sp.parse(fh_sprot):
        if taxon_id in rec.taxonomy_id: # SELECTS records that are related to a specific taxon_id such as 559292 for yeast
            for ac in range(len(rec.accessions)): # Going over each of the entries of the accessions list
                knownProt = "" # knownProt is an indicator to detect whether the current sprot protein is already in GOA file
                if rec.accessions[ac] in goa_dict.keys():
                    knownProt = rec.accessions[ac]
                        # If the current sprot protein is already in the GOA file, the sprot protein is assigned to knownProt 
                    break
            for crossRef in rec.cross_references: # Going over the list of GO information
                if crossRef[0] == 'GO': # consider the cross_reference entries that relate to GO DB
                    goList = [crossRef[1], (crossRef[3].split(':'))[0], crossRef[2][0]]
                    # goList is a list of GO ID, Aspect, and Evidence
                    if (not knownProt) or (knownProt and goList not in goa_dict[knownProt]):# Checking whether a new GO annotaion found
                        # A new GO annotation is found in two situations:
                        # 1. if knownProt is empty  (not knownProt) or
                        # 2. if knownProt is not empty but the GO annotation is not found in the GOA file
                        goaRec = swissProt2GOA(rec, crossRef, GAFFIELDS) # Convert the sprot record to a GOA record
                        GOAParser.writerec(goaRec, fh_merged_go, GAFFIELDS) # Write the converted GOA record to the output file
#                        if goCount in range(1, 20) or goCount in range(6400, 6420):
#                            print ('goCount: ' + str(goCount) + '\n')
#                            goaRec = swissProt2GOA(rec, crossRef, GAFFIELDS) # Convert the sprot record to a GOA record
                        goCount += 1

if __name__ == '__main__':
    print (__doc__)
    sys.exit(0)
