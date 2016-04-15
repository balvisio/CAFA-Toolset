#!/usr/bin/env python

'''
    This module has a set of methods to facilitate fetching records 
    from a UniprotKB/SwissProt file and appending them at the end of 
    a UniProt-GOA file. The main method (entry point) of this module 
    is appendSprot2goa() method which invokes other the methods 
    that are also defined in this module:

    appendSprot2goa(fh_sprot, goa_file_name, taxon_id, fh_merged_go):
        fh_sport: file handle to a UniProtKB/SwissProt file.
        goa_file_name: file name of a UniProt-GOA file.
        taxon_id: a taxonomy id for an organism.
        fh_merged_go: file handle to the output file which already has 
            all the records copied into from the UniProt-GOA file named 
            goa_file_name.
        This method goes over each record in fh_sprot file, checks
        whether that record is already in the UniProt-GOA file
        goa_file_name, and if it is NOT found there, the method
        coverts the UniProtKB/SwissProt record to a UniProt-GOA record
        by invoking swissProt2GOA and then appends the newly formed 
        UniProt-GOA record at the end of the output file.

    create_iterator: 
        It returns an iterator object for an input UniProt-GOA file along
        with a list of all fieldnames of the UniProt-GOA file. 

    swissProt2GOA(sprotRec, crossRef, fields=GOAParser.GAF20FIELDS):
        This method extracts the required information from a 
        UniProtKB/SwissProt record and construct a UniProt-GOA record. 
        It invokes other methods defined in this module to extract 
        the different fields from the SwissProt record. At the end,
        it returns the newly constructed UniProt-GOA record.

    The following methods facilitate swissProt2GOA method to construct the
    UniProt-GOA record by extracting information from a UniProtKB/SwissProt
    record: 

    assignSymbol(sprotRec)
        This method extracts the information from the UniProtKB/SwissProt 
        record that is equivalent to 'DB_Object_Symbol' field of 
        UniProt-GOA file and then returns it.
    
    assignDB_REF(sprotRec, crossRef)
        This method extracts information from the SwissProt record that is
        equivalent to 'DB:Reference' field of UniProt-GOA file. It follows
        the rules from ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/UNIPROT/README
        to construct this field. It invokes the following other methods:

        find_pubmed(sprotRec)
            This method returns the pubmed id from the SwissProt record.

        find_doi(sprotRec)
            This method returns the DOI from the SwissProt record.

        find_reactome_id(sprotRec)
            This method returns REACTOM id from the SwissProt record.

        assignGO_REF(sprotRec, crossRef)
            This method returns an empty string at this point.

    assignSynonym(sprotRec)
        This method extracts information from the SwissProt record that is
        equivalent to 'DB_Object_Synonym' field of UniProt-GOA file. It
        follows the rules from 
        ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/UNIPROT/README to construct 
        this field.

    assignTaxoId(sprotRec)
        This method extracts information from the SwissProt record that is
        equivalent to 'Taxon_ID' field of UniProt-GOA file and the returns it.

    assignDate(sprotRec)
        This method extracts information from the SwissProt record that is
        equivalent to 'Date' field of UniProt-GOA file and then returns it.
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

Months = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', \
              'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def assignSymbol(sprotRec): 
    symbol = ''
# scenario 1: gene_name=> Name=DBP5; Synonyms=RAT8; OrderedLocusNames=YOR046C;
# scenario 2: gene_name=> Name=DCS2 {ECO:0000312|SGD:S000005699};
#                         OrderedLocusNames=YOR173W; ORFNames=O3625;
# scenario 3: gene_name=> Name=DDI2; OrderedLocusNames=YFL061W;
    for g in sprotRec.gene_name.strip(';').split(';'):
        if not g or g.find('=') == -1:
            continue
        # Split each memmber of the group g to a list:
        for f in g.split('=')[1].split(','):
            symbol = ((f.split(' '))[0]).strip()
            break
        # the symbol happens to be not found in the above group g:
        if not symbol and not symbol.isspace():
            continue
        else:
            break
    return symbol

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
# Scenario 1: entry_name=> DBP5_YEAST
# Scenario 2: entry_name=> DCS2_YEAST
# Scenario 3: entry_name=> DDI2_YEAST
    synonym.append(sprotRec.entry_name)
# Scenario 1: gene_name=> Name=DBP5; Synonyms=RAT8; OrderedLocusNames=YOR046C;
# Scenario 2: gene_name=> Name=DCS2 {ECO:0000312|SGD:S000005699}; 
#                         OrderedLocusNames=YOR173W; ORFNames=O3625;
# Scenario 3: gene_name=> Name=DDI2; OrderedLocusNames=YFL061W;
    for g in sprotRec.gene_name.strip(';').split(';'):
        if not g or g.find('=') == -1:
            continue 
        # Split each memmber of the group g to a list:
        for f in g.split('=')[1].split(','): 
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
  
    if (datetime(int(yy_1), Months.index(mm_1),int(dd_1)) < \
        datetime(int(yy_2), Months.index(mm_2), int(dd_2))):
        date = yy_2 + str(Months.index(mm_2)) + dd_2
    else:
        date = yy_1 + str(Months.index(mm_1)) + dd_1
    return date

def swissProt2GOA(sprotRec, crossRef, fields=GOAParser.GAF20FIELDS):
    """
     This method takes a SwissProt record and GO term information
     (crossRef) as input arguments. It then constructs a GOA
     dictionary using the 'fields' as keys and values taken from
     sprotRec, and then returns the constructed GOA record.
    """

    # 15 fields are defined for GAF10FIELDS (GAF 1.0):
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
    # Two extra fields are defined for GAF20FIELDS (GAF 2.0):
    if len(fields) == 17:
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
     This method reads each reacord from the UniProtKB/SwissProt file
     and checks wither it's for taxon_id. If it is, this method
     then checks whether the GO term exists in the UniProt-GOA file
     passed as the file name goa_file_name. If it is a new GO term, 
     this method invokes swissProt2GOA method for each such GO term 
     to construct a UniProt-GOA record which it appends at the end of 
     the merged UniProt-GOA file passed as file handle fh_merged_go. 
    """
    # Creates an iterator object for t1 file:
    iter_handle, GAFFIELDS = create_iterator(goa_file_name) 

    # Construct a dictionary goa_dict with the proteins and 
    # the corresponding GO terms in t1 file:
    goa_dict = {}
    for ingen in iter_handle:
        if ingen['DB_Object_ID'] in goa_dict.keys():
            goa_dict[ingen['DB_Object_ID']].append([ingen['GO_ID'], \
                            ingen['Evidence'], ingen['Aspect']])
        else:
            goa_dict[ingen['DB_Object_ID']] = [[ingen['GO_ID'], \
                           ingen['Evidence'], ingen['Aspect']]]

    # EXTRACTS the NEW GO terms in t2 file that are NOT found in t1 file:
    goCount = 0
    for rec in sp.parse(fh_sprot):
        # SELECTS records that are related to a specific taxon_id
        # such as 559292 for yeast:
        if taxon_id in rec.taxonomy_id:
            # Going over each of the entries of the accessions list:
            for ac in range(len(rec.accessions)):
                # knownProt is an indicator to detect whether the
                # current sprot protein is already in GOA file:
                knownProt = ""
                if rec.accessions[ac] in goa_dict.keys():
                    # If the current sprot protein is already in the GOA
                    # file, the sprot protein is assigned to knownProt:
                    knownProt = rec.accessions[ac]
                    break
            # Going over the list of GO information:
            for crossRef in rec.cross_references:
                # Consider the cross_reference entries that relate to GO DB:
                if crossRef[0] == 'GO':
                    # goList is a list of GO ID, Aspect, and Evidence:
                    goList = [crossRef[1], (crossRef[3].split(':'))[0], \
                              crossRef[2][0]]
                    # Checking whether a new GO annotaion found:
                    if (not knownProt) or (knownProt and \
                        goList not in goa_dict[knownProt]):
                        # A new GO annotation is found in two situations:
                        # 1. if knownProt is empty  (not knownProt) or
                        # 2. if knownProt is not empty but the GO annotation
                        #    is not found in the GOA file

                        # Convert the sprot record to a GOA record:
                        goaRec = swissProt2GOA(rec, crossRef, GAFFIELDS)
                        # Write the converted GOA record to the output file:
                        GOAParser.writerec(goaRec, fh_merged_go, GAFFIELDS)
#                        if goCount in range(1, 20) or goCount in range(6400, 6420):
#                            print ('goCount: ' + str(goCount) + '\n')
#                            goaRec = swissProt2GOA(rec, crossRef, GAFFIELDS)
                        goCount += 1
    return goCount
if __name__ == '__main__':
    print (sys.argv[0] + ':')
    print (__doc__)
    sys.exit(0)
