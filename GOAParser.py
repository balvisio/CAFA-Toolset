#!/usr/bin/env python
"""
    This method defines the following dictionaries and methods
    related to UniProt-GOA files: 

    GAF20FIELDS 
        List of the fields of Gene Association File (GAF) Format version 2.0
        Details: http://geneontology.org/page/go-annotation-file-format-20

    GAF10FIELDS 
        List of the fields of Gene Association File (GAF) Format version 1.0
        Details: http://geneontology.org/page/go-annotation-file-gaf-format-10

    GPA10FIELDS
        List of the fields of Gene Product Association Data (GPAD) 
            Format version 1.0
        Details: 
        http://geneontology.org/page/gene-product-association-data-gpad-format

    GPA11FIELDS
        List of the fields of Gene Product Association Data (GPAD) Format version 1.1
        Details: 
        http://geneontology.org/page/gene-product-association-data-gpad-format

    GPI10FIELDS
        List of the fields of Gene Product Information (GPI) Format version 1.0
        Details: http://geneontology.org/page/gene-product-information-gpi-format

    GPI11FIELDS
        List of the fields of Gene Product Information (GPI) Format version 1.1
        Details: http://geneontology.org/page/gene-product-information-gpi-format
      
    _gpi10iterator(handle)
        This method returns an iterator to read a file in GPI format version 1.0 
       
    _gpi11iterator(handle)
        This method returns an iterator to read a file in GPI format version 1.1 

    gpi_iterator(handle):
        This method invokes _gpi10iterator or _gpi11iterator private methods
        based on GPI file format version and retuns an iterator to read a file
        either in GPI format version 1.0 or 1.1

    _gpa10iterator(handle):
        This method returns an iterator to read a file in GPA format 
        version 1.0

    _gpa11iterator(handle):
        This method returns an iterator to read a file in GPA format 
        version 1.1

    gpa_iterator(handle):
        This method invokes _gpa10iterator or _gpa11iterator private methods
        based on GPA file format version and retuns an iterator to read a file
        either in GPA format version 1.0 or 1.1

    _gaf20iterator(handle):
        This method returns an iterator to read a file in GAF format 
        version 2.0

    _gaf10iterator(handle):
        This method returns an iterator to read a file in GAF format 
        version 1.0

    gafiterator(handle):
        This method invokes _gaf10iterator or _gaf20iterator private methods
        based on GAF file format version and retuns an iterator to read a file
        either in GAF format version 1.0 or 2.0

    _gaf10byproteiniterator(handle):


    _gaf20byproteiniterator(handle):

    gafbyproteiniterator(handle):
        This method invokes _gaf10byproteiniterator or _gaf20byproteiniterator
        private methods based on GAF file format version and retuns an 
        iterator to read a file either in GAF format version 1.0 or 2.0.
        The iterator goes over the consecutive records with the same 
        DB_OBJECT_ID. 

    writerec(outrec,handle,fields=GAF20FIELDS)
        This method writes a single UniProt-GOA reacord to an output file
        stream.    

    writebyproteinrec(outprotrec,handle,fields=GAF20FIELDS)
        This method writes a list of UniProt-GOA records to an output file 
        stream. 

    record_has(inrec, fieldvals)
        This method accepts a record and a dictionary of filed values. 
        The function returns: 
            True, if any filed of the record has a matching
            False, otherwise 

    Some useful websites: 

    Uniprot-GOA README with  GAF format description:
    ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/UNIPROT/README

    List of all GOA file formats:
    http://www.geneontology.org/GO.format.annotation.shtml

"""
import copy
import sys

# GAF version 2.0
GAF20FIELDS = ['DB' , 
        'DB_Object_ID' , 
        'DB_Object_Symbol' , 
        'Qualifier' , 
        'GO_ID' , 
        'DB:Reference' , 
        'Evidence' , 
        'With' , 
        'Aspect',
        'DB_Object_Name' , 
        'Synonym' , 
        'DB_Object_Type' , 
        'Taxon_ID' , 
        'Date' , 
        'Assigned_By' , 
        'Annotation_Extension' , 
        'Gene_Product_Form_ID']

# GAF version 1.0
GAF10FIELDS = ['DB' , 
        'DB_Object_ID' , 
        'DB_Object_Symbol' , 
        'Qualifier' , 
        'GO_ID' , 
        'DB:Reference' , 
        'Evidence' , 
        'With' , 
        'Aspect',
        'DB_Object_Name' , 
        'Synonym' , 
        'DB_Object_Type' , 
        'Taxon_ID' , 
        'Date' , 
        'Assigned_By'] 

# GPA version 1.0
GPA10FIELDS = [
      'DB',
      'DB_Object_ID',
      'Qualifier',
      'GO_ID',
      'DB:Reference',
      'Evidence code',
      'With',
      'Interacting_taxon_ID',
      'Date',
      'Assigned_by',
      'Annotation_Extension',
      'Spliceform_ID']

# GPA version 1.1
GPA11FIELDS = [
      'DB',
      'DB_Object_ID',
      'Qualifier',
      'GO_ID',
      'DB:Reference',
      'ECO_Evidence_code',
      'With',
      'Interacting_taxon_ID',
      'Date',
      'Assigned_by',
      'Annotation Extension',
      'Annotation_Properties']

# GPI version 1.0
GPI10FIELDS = [
      'DB',
      'DB_subset',
      'DB_Object_ID',
      'DB_Object_Symbol',
      'DB_Object_Name',
      'DB_Object_Synonym',
      'DB_Object_Type',
      'Taxon',
      'Annotation_Target_Set',
      'Annotation_Completed',
      'Parent_Object_ID']

# GPI version 1.1
GPI11FIELDS = [
      'DB_Object_ID',
      'DB_Object_Symbol',
      'DB_Object_Name',
      'DB_Object_Synonym',
      'DB_Object_Type',
      'Taxon',
      'Parent_Object_ID',
      'DB_Xref',
      'Gene_Product_Properties',
      'Annotation_Target_Set',
      'GO_Annotation_Complete']

def _gpi10iterator(handle):
    """
    Read GPI 1.0 format files (PRIVATE).
    This iterator is used to read a gp_information.goa_uniprot
    file which is in the GPI 1.0 format.
    """
    for inline in handle:
        if inline[0] == '!': continue
        inrec = inline.rstrip('\n').split('\t')
        if len(inrec) == 1:
            continue
        inrec[5] = inrec[5].split('|') # DB_Object_Synonym(s)
        inrec[8] = inrec[8].split('|') # Annotation_Target_Set
        yield dict(zip(GPI10FIELDS, inrec))

def _gpi11iterator(handle):
    """
    Read GPI 1.0 format files (PRIVATE).
    This iterator is used to read a gp_information.goa_uniprot
    file which is in the GPI 1.0 format.
    """
    for inline in handle:
        if inline[0] == '!': continue
        inrec = inline.rstrip('\n').split('\t')
        if len(inrec) == 1:
            continue
        inrec[2] = inrec[2].split('|') # DB_Object_Name
        inrec[3] = inrec[3].split('|') # DB_Object_Synonym(s)
        inrec[7] = inrec[7].split('|') # DB_Xref(s)
        inrec[8] = inrec[8].split('|') # Properties
        yield dict(zip(GPI11FIELDS, inrec))

def gpi_iterator(handle):
    """
    This method reads a GPI format file. This function should be called 
    to read a gp_information.goa_uniprot file. At the moment, there is
    only one format, but this may change, so this function is a placeholder 
    a future wrapper.
    """
    inline = handle.readline()
    if inline.strip() == '!gpi-version: 1.1':
        sys.stderr.write("gpi 1.1\n")
        return _gpi11iterator(handle)
    else:
        sys.stderr.write("gpi 1.0\n")
        return _gpi10iterator(handle)

def _gpa10iterator(handle):
    """
    Read GPA 1.0 format files (PRIVATE).
    This iterator is used to read a gp_association.*
    file which is in the GPA 1.0 format. Do not call directly. 
    Rather, use the gpaiterator function.
    """

    for inline in handle:
        if inline[0] == '!': continue
        inrec = inline.rstrip('\n').split('\t')
        if len(inrec) == 1:
            continue
        inrec[2] = inrec[2].split('|') # Qualifier
        inrec[4] = inrec[4].split('|') # DB:Reference(s)
        inrec[6] = inrec[6].split('|') # With
        inrec[10] = inrec[10].split('|') # Annotation extension
        yield dict(zip(GPA10FIELDS, inrec))

def _gpa11iterator(handle):
    """
    Read GPA 1.1 format files (PRIVATE).
    This iterator is used to read a gp_association.goa_uniprot
    file which is in the GPA 1.1 format. Do not call directly. Rather
    use the gpa_iterator function
    """
    for inline in handle:
        if inline[0] == '!': continue
        inrec = inline.rstrip('\n').split('\t')
        if len(inrec) == 1:
            continue
        inrec[2] = inrec[2].split('|') # Qualifier
        inrec[4] = inrec[4].split('|') # DB:Reference(s)
        inrec[6] = inrec[6].split('|') # With
        inrec[10] = inrec[10].split('|') # Annotation extension
        yield dict(zip(GPA11FIELDS, inrec))

def gpa_iterator(handle):
    """
    Wrapper function: read GPA format files.
    This function should be called to read a
    gene_association.goa_uniprot file. Reads the first record and
    returns a gpa 1.1 or a gpa 1.0 iterator as needed
    """
    inline = handle.readline()
    if inline.strip() == '!gpa-version: 1.1':
        sys.stderr.write("gpa 1.1\n")
        return _gpa11iterator(handle)
    else:
        sys.stderr.write("gpa 1.0\n")
        return _gpa10iterator(handle)

def _gaf20iterator(handle):
    for inline in handle:
        if inline[0] == '!': continue
        inrec = inline.rstrip('\n').split('\t')
        if len(inrec) == 1:
            continue
        inrec[3] = inrec[3].split('|') #Qualifier
        inrec[5] = inrec[5].split('|') # DB:reference(s)
        inrec[7] = inrec[7].split('|') # With || From
        inrec[10] = inrec[10].split('|') # Synonym
        inrec[12] = inrec[12].split('|') # Taxon
        yield dict(zip(GAF20FIELDS, inrec))


def _gaf10iterator(handle):
    for inline in handle:
        if inline[0] == '!': continue
        inrec = inline.rstrip('\n').split('\t')
        if len(inrec) == 1:
            continue
        inrec[3] = inrec[3].split('|') #Qualifier
        inrec[5] = inrec[5].split('|') # DB:reference(s)
        inrec[7] = inrec[7].split('|') # With || From
        inrec[10] = inrec[10].split('|') # Synonym
        inrec[12] = inrec[12].split('|') # Taxon
        yield dict(zip(GAF10FIELDS, inrec))

def _gaf10byproteiniterator(handle):
    cur_id = None
    id_rec_list = []
    for inline in handle:
        if inline[0] == '!': continue
        inrec = inline.rstrip('\n').split('\t')
        if len(inrec) == 1:
            continue
        inrec[3] = inrec[3].split('|') #Qualifier
        inrec[5] = inrec[5].split('|') # DB:reference(s)
        inrec[7] = inrec[7].split('|') # With || From
        inrec[10] = inrec[10].split('|') # Synonym
        inrec[12] = inrec[12].split('|') # Taxon
        cur_rec = dict(zip(GAF10FIELDS, inrec))
        if cur_rec['DB_Object_ID'] != cur_id and cur_id:
            ret_list = copy.copy(id_rec_list)
            id_rec_list = [cur_rec]
            cur_id = cur_rec['DB_Object_ID']
            yield ret_list
        else:
            cur_id = cur_rec['DB_Object_ID']
            id_rec_list.append(cur_rec)

def _gaf20byproteiniterator(handle):
    cur_id = None
    id_rec_list = []
    for inline in handle:
        if inline[0] == '!': continue
        inrec = inline.rstrip('\n').split('\t')
        if len(inrec) == 1:
            continue
        inrec[3] = inrec[3].split('|') #Qualifier
        inrec[5] = inrec[5].split('|') # DB:reference(s)
        inrec[7] = inrec[7].split('|') # With || From
        inrec[10] = inrec[10].split('|') # Synonym
        inrec[12] = inrec[12].split('|') # Taxon
        cur_rec = dict(zip(GAF20FIELDS, inrec))
        if cur_rec['DB_Object_ID'] != cur_id and cur_id:
            ret_list = copy.copy(id_rec_list)
            id_rec_list = [cur_rec]
            cur_id = cur_rec['DB_Object_ID']
            yield ret_list
        else:
            cur_id = cur_rec['DB_Object_ID']
            id_rec_list.append(cur_rec)

def gafbyproteiniterator(handle):
    """
    Iterates over records in a gene association file. 
    Returns a list of all consecutive records with the same DB_Object_ID
    This function should be called to read a
    gene_association.goa_uniprot file. Reads the first record and
    returns a gaf 2.0 or a gaf 1.0 iterator as needed
    """
    inline = handle.readline()
    if inline.strip() == '!gaf-version: 2.0':
        sys.stderr.write("gaf 2.0\n")
        return _gaf20byproteiniterator(handle)
    else:
        sys.stderr.write("gaf 1.0\n")
        return _gaf10byproteiniterator(handle)

def gafiterator(handle):
    """
    Iterate pver a GAF 1.0 or 2.0 file.
    This function should be called to read a
    gene_association.goa_uniprot file. Reads the first record and
    returns a gaf 2.0 or a gaf 1.0 iterator as needed
    """
    inline = handle.readline()
    if inline.strip() == '!gaf-version: 2.0':
        sys.stderr.write("gaf 2.0\n")
        return _gaf20iterator(handle)
    else:
        sys.stderr.write("gaf 1.0\n")
        return _gaf10iterator(handle)

def writerec(outrec,handle,fields=GAF20FIELDS):
    """Write a single UniProt-GOA record to an output stream. 

    Caller should know the  format version. Default: gaf-2.0
    If header has a value, then it is assumed this is the first record,
    a header is written.
    """
    outstr = ''
    for field in fields[:-1]:
        if isinstance(outrec[field], list):
            for subfield in outrec[field]:
                outstr += subfield + '|'
            outstr = outstr[:-1] + '\t'
        else:
            outstr += outrec[field] + '\t'
    outstr += outrec[fields[-1]] + '\n'
    handle.write("%s" % outstr)

def writebyproteinrec(outprotrec,handle,fields=GAF20FIELDS):
    """
    Write a list of GAF records to an output stream. 
    Caller should know the  format version. Default: gaf-2.0
    If header has a value, then it is assumed this is the first record,
    a header is written. Typically the list is the one read by 
    fafbyproteinrec, which contains all consecutive lines with the 
    same DB_Object_ID
    """
    for outrec in outprotrec:
        writerec(outrec, handle, fields=fields)

def record_has(inrec, fieldvals):
    """
    This method accepts a record, and a dictionary of field values. 
    The format is {'field_name': set([val1, val2])}.
    If any field in the record has a matching value, the function returns
    True. Otherwise, returns False.
    """
    retval = False
    for field in fieldvals:
        if isinstance(inrec[field], str):
            set1 = set([inrec[field]])
        else:
            set1 = set(inrec[field])
        if (set1 & fieldvals[field]):
            retval = True
            break
    return retval

if __name__ == '__main__':
    print (sys.argv[0] + ':')
    print(__doc__)
    sys.exit(0)
