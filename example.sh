#!/bin/sh 

# This is an example shell script to run the CAFA tools 

#Download the uniprot_sprot.dat.2014_09 file that will be used by the software
curDir=$(pwd)
fileName="uniprot_sprot.dat.2014_09"
if [ ! -f ${curDir}'/'${fileName} ] && [ ! -f ${curDir}'/workspace/'${fileName} ]; then
   echo 'Downloading ...'
   wget ftp://ftp.uniprot.org/pub/databases/uniprot/previous_releases/release-2014_09/knowledgebase/uniprot_sprot-only2014_09.tar.gz
   gzip -d uniprot_sprot-only2014_09.tar.gz
   tar xvf uniprot_sprot-only2014_09.tar
   gzip -d uniprot_sprot.dat.gz
   echo 'Renaming'  uniprot_sprot.dat.gz 'to' $fileName 
   mv uniprot_sprot.dat uniprot_sprot.dat.2014_09
   echo 'Deleting redundant downloaded files ...'
   rm uniprot_sprot-only2014_09.tar
   rm uniprot_sprot_varsplic.fasta.gz 
   rm uniprot_sprot.xml.gz
   rm uniprot_sprot.fasta.gz
fi

# Integrating Annotation Datasets
# The following command will create an output file by appending the protein annotaitons 
# found in uniprot_sprot.dat.38 but not in gene_association.goa_ref_yeast.38+sprot.38 
# at the end of the second file

python Mergedb -I1=uniprot_sprot.dat.2014_09 -I2=gene_association.goa_ref_yeast.38 -G 559292 

# Output file: gene_association.goa_ref_yeast.38+sprot.2014_09  

# Target Generation 
# The following command will create a target file with the protein sequences from the input 
# file uniprot_sprot.dat.2014_09

python Filter -I1=uniprot_sprot.dat.2014_09  -G=559292 

# Output file name: uniprot_sprot.dat.2014_09.559292.tfa.1 

## Benchmark Creation
# The following command creates benchmark files based on two input annotation files

python Benchmark -I1=gene_association.goa_ref_yeast.23 -I2=gene_association.goa_ref_yeast.52

# This command will create six benchmark files:
# 1. gene_association.goa_ref_yeast.52-23.benchmark_LK_bpo.1 
# 2. gene_association.goa_ref_yeast.52-23.benchmark_LK_cco.1
# 3. gene_association.goa_ref_yeast.52-23.benchmark_LK_mfo.1
# 4. gene_association.goa_ref_yeast.52-23.benchmark_NK_bpo.1
# 5. gene_association.goa_ref_yeast.52-23.benchmark_NK_cco.1
# 6. gene_association.goa_ref_yeast.52-23.benchmark_NK_mfo.1 

# Files (1) – (3) are limited knowledge (LK) benchmark files in biological process ontology (bpo), 
# cellular component ontology (cco), and molecular function ontology (mfo), respectively. 
# Files (4) – (6) are three no-knowledge (NK) benchmark files for these ontologies (bpo, cco, 
# and mfo), respectively.


## Benchmark Verification
# This following command will verify the benchmark files just created
python Verify -I1=gene_association.goa_ref_yeast.23 -I2=gene_association.goa_ref_yeast.52 -I3=gene_association.goa_ref_yeast.52-23.benchmark_LK_bpo.1
