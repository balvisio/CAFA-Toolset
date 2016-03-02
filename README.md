<<<<<<< HEAD
## CAFA Toolset 
#### Features 
* Integration of protein annotation databases: This tool integrates multiple protein annotation datasets in different file 
formats into one larger dataset. Current release merges two datasets, one in unprot-SwissProt format and the other in 
uniprot-GOA format, into a larger single dataset in uniprot-GOA format.
* Target generation: This tool generates a set of protein sequences in fasta file format that will be sent out to the community 
participating in the CAFA challenge.
* Benchmark creation and verification: This tool creates the benchmark protein sets for the CAFA challenge.
* Assessment of protein annotation prediction models: This tool evaluates the protein annotation prediction models submitted 
by the participants in the CAFA challenge.

### Introduction

This software is developed to facilitate the Critical Annotation of protein Function Annotation (CAFA) experiment 
and can be useful to anyone engaged in protein function prediction research. CAFA evaluates and ranks the prediction 
algorithms based on their ability to predict Gene Ontology (GO) and Human Phenotype Ontology (HPO) terms for a given 
set of protein sequences. The GO terms can be in any of the following three categories: Molecular Function Ontology (MFO), 
Biological Process Ontology (BPO), and Cellular Component Ontology (CCO). Here is the link for  CAFA 
rules: http://biofunctionprediction.org/node/8. The following figure shows the CAFA time-line.

![Alt CAFA time line] (/figures/cafa-timeLine.png?raw=true “CAFA Timeline”)

This software is specifically designed for the participants in the upcoming CAFA 3 experiment. The CAFA 1 results are 
published in Radivojac P et al, Nature Methods 2013 (PMID 23353650) and CAFA 2 results are submitted for publication.

Definitions of some terms used in this document are given as follows.

#### Time points t0, t1, and t2
t0 is the time point when a CAFA experiment is launched and targets are made accessible to the community, whereas t1 is 
the time point set as the deadline for submitting the prediction models by the CAFA participants. Farther along the time line, 
the time point t2 is when the benchmarks are collected for the evaluation of the submitted prediction models.

The CAFA experiment is designed around the dynamic growth property of the protein annotation databases. After launching CAFA 
at time t0, the modelers are given some time to use this property to develop and test their algorithms. Subsequently, after the 
submission of the prediction models is closed at time t1, the annotation databases are given an ample amount of time from t1 to t2 
before collecting the benchmarks so that those databases can accumulate enough annotations with experimental evidence codes.

#### Target set
It is the large collection of protein sequences released at time point t0 when the CAFA challenge is announced.

#### Benchmark set
It is a set of proteins whose functions were, until recently, unknown. Protein annotations at two time points, t1 and t2, are collected from 
the annotation databases such as uniProt-GOA or uniProt-swissProt, and the annotations that gained experimental evidence at time t2 are 
placed in the benchmark set. Two types of benchmark sets, no-knowledge and limited-knowledge, are used in each of the three ontologies 
(MFO, BPO, and CCO) to evaluate the protein function prediction models. Thus, we can have total six types of benchmark sets.

##### No-knowledge (NK) benchmark set
A protein will be included in this set if it did not have any experimentally verified annotations in any of the GO ontologies (MFO, BPO, CCO) 
at time t1 but has gained at least one experimentally verified functional term in a specific ontology between t1 and t2. Therefore, we will 
have three NK benchmark sets – one for each ontology.

##### Limited-knowledge (LK) benchmark set
A protein will be included in this set if it did not have any experimentally verified annotations in a 
specific GO ontology, such as MFO, (irrespective of whether it had such annotations in one or both of the other two ontologies) at t1 
but has gained at least one experimentally verified functional term in that specific ontology between t1 and t2. Therefore, we will 
have three LK benchmark sets – one for each ontology.

##### GAF 1.0 vs GAF 2.0
These are two file formats for uniprot-goa annotation files. The input annotation files must be in either one of 
these two file formats for Benchmark creation and verification tools. More details fro GAF 1.0 formate can be found at
http://geneontology.org/page/go-annotation-file-gaf-format-10 and more details about GAF 2.0 format can be found at
http://geneontology.org/page/go-annotation-file-format-20.

### Python Requirements
* Python 2.7 
* Biopython 1.66 or greater 

### Software Usage 

##### Script to test run the commands for CAFA Toolset
The commands in this help file can be found in the script example.sh. One can test the commands for this toolset simply by executing 
this script at a linux promt as follows: 

##### sh example.sh

Below one can find the detailed usage description of each feature of the CAFA toolset.

### Benchmark Creation
This tool will create benchmark files from two input annotation files in uniprot-GOA file format at time points t1 and t2, respectively. 
The simplest way to run this program:

python Benchmark  --input1 uniprot-goa-annotation-at-t1 --input2 uniprot-goa-annotation-at-t2

input 1 and input 2 are two annotation files at time points t1 and t2, respectively. Each of the input files must be in 
GAF 1.0 or GAF 2.0 format. Here is an example with gene_association.goa_ref_yeast.23 and gene_association.goa_ref_yeast.52 
as the annotation files at time points t1 and t2, respectively.

##### python Benchmark -I1=gene_association.goa_ref_yeast.23 -I2=gene_association.goa_ref_yeast.52

It will create six benchmark files: 

1. gene_association.goa_ref_yeast.52.benchmark_LK_bpo.1

2. gene_association.goa_ref_yeast.52.benchmark_LK_cco.1

3. gene_association.goa_ref_yeast.52.benchmark_LK_mfo.1

4. gene_association.goa_ref_yeast.52.benchmark_NK_bpo.1

5. gene_association.goa_ref_yeast.52.benchmark_NK_cco.1

6. gene_association.goa_ref_yeast.52.benchmark_NK_mfo.1 

Files (1) – (3) are limited knowledge (LK) benchmark files in BPO, CCO, and MFO categories, respectively. Files (4) – (6) are three 
no-knowledge (NK) benchmark files in these ontologies (BPO, CCO, and MFO), respectively. Running this tool multiple times with 
the same input file name at time point t2, will create the benchmark files ending with the subseqent version number such as 
2, 3, 4 etc. in consecutive runs.

### Benchmark Verification
This tool will verify the benchmark files generated by the Benchmark Creation tool. The simplest way to run the program:

python Verify --input1 uniprot-goa-annotation-at-t1 --input2 uniprot-goa-annotation-at-t2

input 1 and input 2 are two annotation files at time points t1 and t2, respectively. Each of the input files must be in GAF 1.0 or 
GAF 2.0 format. Here is an example with gene_association.goa_ref_yeast.23 and gene_association.goa_ref_yeast.52 as the input
annotation files at time points t1 and t2, respectively.

##### python Verify -I1=gene_association.goa_ref_yeast.23 -I2=gene_association.goa_ref_yeast.52

The program will find the SIX benchmark files of the latest version (obtained from the last run of Benchmark in benchmark creation
mode) and verify the content in each of them for the correctness of the benchmark entries. To verify the benchmark files of a specific 
version, you can supply any of the benchmark files as the third input. That way, the program will verify all the benchmark files ending
with that specific version number available in the work space folder. Here is an example for verifying the benchmark files of a specific
version number (version 1):

##### python Verify -I1=gene_association.goa_ref_yeast.23 -I2=gene_association.goa_ref_yeast.52 -I3=gene_association.goa_ref_yeast.52.benchmark_LK_bpo.1

You must also supply all the optional parameters that you supplied while running the Benchmark Creation program to create this version 
of the benchmark files. This will verify all six benchmark files ending with .1 i.e dot one.

### Target Generation
This tool will create a a file for the target set, containing the protein sequences in fasta format. The simplest way to run the program for target generation:

python Benchmark  -M TG --input1 uniprot-goa-annotation-at-t0 --input2 uniprot-goa-annotation-information-at-t0

input1 is a uniprot-GOA annotation file in gaf format at a certain time point (in cafa competition, this is time t0, the sequence release date 
for the CAFA experiment). Input2 is a uniprot-GOA file in gpi format that supplies additional information about the input1 file at the same time point. 
Here is an example with gene_association.goa_ref_yeast.23 as the GOA annotation file and gp_information.goa_ref_yeast.23  as the gpi file with 
the additional information about that GOA file (both retrieved from uniprot-GOA archive).

##### python Benchmark -M TG -I1=gene_association.goa_ref_yeast.23 -I2=gp_information.goa_ref_yeast.23

The program will generate THREE target sequence files in fasta format (one file for each ontology) for a supplied taxon with the amino acid sequences 
of the proteins having no experimental evidence (evidence code IEA).

1. gene_association.goa_ref_yeast.23.target_taxa_559292_bpo.1.fasta
2. gene_association.goa_ref_yeast.23.target_taxa_559292_cco.1.fasta
3. gene_association.goa_ref_yeast.23.target_taxa_559292_mfo.1.fasta

In this target generation mode, only optional parameter is targetType. Be default, it is set to 0, which means only IEA exclusive proteins would be considered 
for being potential targets.

### Source Code
This is an open source project and the source code is publicly available on github through the following url: https://github.com/arkatebi/CAFA-Benchmark. 
For questions, please email us: Iddo Friedberg (idoerg@gmail.com) or Ataur Katebi (arkatebi@gmail.com).





=======
# CAFA-Toolset
A software package for managing the CAFA community experiment
>>>>>>> c2671a5eaa2ac9da800d17be16538a0badcc0b0e
