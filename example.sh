#!/bin/sh

# This is an example shell script to run the CAFA tools 

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

## Target generation
# The following command will create target sequence files. 
# It is commented out because it takes a long time to download the seuqences. 
# Please, uncomment the following command to generate the target sequences.

# python Benchmark -M TG -I1=gene_association.goa_ref_yeast.23 -I2=gp_information.goa_ref_yeast.23

# This command will generate the following three fasta files: 

# 1. gene_association.goa_ref_yeast.23.target_taxa_559292_bpo.1.fasta
# 2. gene_association.goa_ref_yeast.23.target_taxa_559292_cco.1.fasta
# 3. gene_association.goa_ref_yeast.23.target_taxa_559292_mfo.1.fasta


