#!/bin/sh

# This is an example shell script to run the CAFA tools 

# Integrating Annotation Datasets
# The following command will create an output file by appending the protein annotaitons 
# found in uniprot_sprot.dat.38 but not in gene_association.goa_ref_yeast.38+sprot.38 
# at the end of the second file

python Mergedb -I1=uniprot_sprot.dat.38 -I2=gene_association.goa_ref_yeast.38 -G 559292 

# Output file: gene_association.goa_ref_yeast.38+sprot.38  

# Target Generation 
# The following command will create a target file with the protein sequences from the input 
# file uniprot_sprot.dat.38

python Filter -I1=uniprot_sprot.dat.38  -G=559292 

# Output file name: uniprot_sprot.dat.38.559292.tfa.1 

## Benchmark Creation
# The following command creates benchmark files based on two input annotation files

python Benchmark -I1=gene_association.goa_ref_yeast.23 -I2=gene_association.goa_ref_yeast.52

# This command will create six benchmark files:
# 1. gene_association.goa_ref_yeast.52.benchmark_LK_bpo.1 
# 2. gene_association.goa_ref_yeast.52.benchmark_LK_cco.1
# 3. gene_association.goa_ref_yeast.52.benchmark_LK_mfo.1
# 4. gene_association.goa_ref_yeast.52.benchmark_NK_bpo.1
# 5. gene_association.goa_ref_yeast.52.benchmark_NK_cco.1
# 6. gene_association.goa_ref_yeast.52.benchmark_NK_mfo.1 

# Files (1) – (3) are limited knowledge (LK) benchmark files in biological process ontology (bpo), 
# cellular component ontology (cco), and molecular function ontology (mfo), respectively. 
# Files (4) – (6) are three no-knowledge (NK) benchmark files for these ontologies (bpo, cco, 
# and mfo), respectively.


## Benchmark verification
# This following command will verify the benchmark files just created

python Verify -I1=gene_association.goa_ref_yeast.23 -I2=gene_association.goa_ref_yeast.52

# The above code can also be executed as below with one of the benchmark files as the third input:

python Verify -I1=gene_association.goa_ref_yeast.23 -I2=gene_association.goa_ref_yeast.52 -I3=gene_association.goa_ref_yeast.52.benchmark_LK_bpo.1


