## CAFA Toolset
#####         A software package for managing the CAFA community experiment 
#### Features 

  1. Integration of protein annotation databases: this tool integrates 
      multiple protein annotation datasets in different file formats into 
      one larger dataset. Current release merges two datasets, one in 
      UniProtKB/SwissProt format and the other in UniProt-GOA format, into 
      a larger single dataset in UniProt-GOA format.

  2. Target generation: this tool generates a set of protein sequences 
       in the FASTA file format that can be used by the scientific community 
       participating in the CAFA challenge or anyone performing research in 
       protein function annotation.

  3. Benchmark creation and verification: this is a twin toolset of which one
     creates the benchmark protein sets for the CAFA challenge and the other
     one verifies those benchmark sets.

  4. Assessment of protein annotation prediction models: this tool evaluates 
      the protein annotation prediction models submitted by the participants 
      in the CAFA challenge.

### Introduction

This software is developed to facilitate the Critical Annotation of protein 
Function Annotation (CAFA) experiment and can be useful to anyone engaged in 
protein function prediction research. CAFA evaluates the strengths and 
weaknesses of the prediction algorithms based on their ability to predict 
Gene Ontology (GO) and Human Phenotype Ontology (HPO) terms for a given set 
of protein sequences. The GO terms can be in any of the following three 
categories: Molecular Function Ontology (MFO), Biological Process Ontology 
(BPO), and Cellular Component Ontology (CCO). The following figure shows the 
CAFA time-line.

![Alt CAFA time line] (/figures/cafa-timeLine.png?raw=true “CAFA Timeline”)

This software is specifically designed for the participants in the upcoming 
CAFA-3 experiment. The CAFA-1 results are published in Nature Methods [1] and CAFA-2 results 
are submitted for publication. 

##### Some informative sites 
* CAFA rules and announcements: http://biofunctionprediction.org/node/8 
* Automated protein function prediction: http://biofunctionprediction.org/
* Function-SIG (formerly AFP-SIG) at ISMB 2016: https://www.iscb.org/ismb2016program/ismb2016-sigs#afp-sig  
* Selected proceedings from AFP meeting 2011: http://bmcbioinformatics.biomedcentral.com/articles/supplements/volume-14-supplement-3 
* News release about CAFA-1: http://miamioh.edu/news/article/view/18233.html
* Evidence code decision tree: http://geneontology.org/page/evidence-code-decision-tree

##### UniProt-GOA 
This is a database for protein assignments to GO resources which maintains a 
dynamically controlled vocabulary. 
*  UniProt-GOA dataset current release: 
   ftp://ftp.ebi.ac.uk/pub/databases/GO/goa
*  UniProt-GOA dataset archive: 
   ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/old
*  UniProt-GOA README:
   http://www.geneontology.org/gene-associations/readme/goa.README
*  List of all GOA file formats: 
   http://geneontology.org/page/go-annotation-file-formats
*  UniProt-GOA file formats:
   ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/UNIPROT/README
*  GAF 1.0 format: http://geneontology.org/page/go-annotation-file-gaf-format-10
*  GAF 2.0 format: http://geneontology.org/page/go-annotation-file-format-20

##### UniProtKB/SwissProt 
This is a non-redundant protein sequence database. Each entry in this database
is manually annotated involving detailed analysis of the protein sequence and
of the scientific literature. The database is recognized as the central access
point of the extensive curated protein information, classification, and
cross-reference.

* Gene counts with experimental annotations in UniProtKB/SwissProt: 
  https://github.com/arkatebi/SwissProt-stats
* UniProtKB/SwissProt dataset current release:
  ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/
* UniProtKB/SwissProt dataset archive (release 46 and greater):
  ftp://ftp.uniprot.org/pub/databases/uniprot/previous_releases/
* UniProtKB/SwissProt dataset archive (release 9 to 45):
  ftp://ftp.ebi.ac.uk/pub/databases/swissprot/sw_old_releases/
* Detailed release statistics:
  http://web.expasy.org/docs/relnotes/relstat.html
* UniProtKB/SwissProt file format:
  http://web.expasy.org/docs/userman.html

### Some Definitions
The definitions of some of the terms used in this document are as follows.

#### Time points t0, t1, t2, and t3
t0 is the time point when a CAFA experiment is launched and targets are made
accessible to the community, whereas t1 is the time point set as the deadline
for submitting the prediction models by the CAFA participants. Farther along
the time line, t2 is the time point when the benchmarks are collected for the
evaluation of the submitted prediction models.

The CAFA experiment is designed around the dynamic growth property of the
protein annotation databases. After launching CAFA at time t0, the modelers
are given some time to use this property for developing and testing their
algorithms. Subsequently, after the submission of the prediction models is
closed at time t1, the annotation databases are given an ample amount of
time from t1 to t2 before collecting the benchmarks so that those databases
can accumulate enough annotations with experimental evidence codes. At time
point t3, the results of the evaluation of the submitted prediction models
are announced.

#### Target set
It is the large collection of protein sequences released at time point t0 
when the CAFA challenge is announced.

#### Benchmark set
It is a set of proteins whose functions were, until recently, unknown.
Protein annotations at two time points, t1 and t2, are collected from the
annotation databases such as UniProt-GOA or UniProtKB/SwissProt, and the
annotations that gained experimental evidence at time t2 are placed in the
benchmark set. Two types of benchmark sets, no-knowledge and
limited-knowledge, are used in each of the three ontological categories
(MFO, BPO, and CCO) to evaluate the protein function prediction models.
Thus, we can have total six types of benchmark sets.

##### No-knowledge (NK) benchmark sets
An NK-benchmark set consists of the proteins that did not have any
experimentally verified annotations in any of the GO ontologies
(MFO, BPO, and CCO) at time t1 but have gained at least one experimentally
verified functional term in a specific ontology between time t1 and t2.
Therefore, we will have three NK-benchmark sets – one for each ontology.

##### Limited-knowledge (LK) benchmark sets
An LK-benchmark set consists of the proteins that did not have any 
experimentally verified annotations in a specific GO ontology (say, MFO) 
but had such annotations in any of the other two ontologies (say, BPO and 
CCO) at time t1 and subsequently gained at least one experimentally verified 
functional term in that specific ontology (MFO) between time t1 and t2. 
Therefore, we will have three LK benchmark sets – one for each ontology.

### Requirements
* Python 3.6
* Biopython 1.79 or greater

### Software Usage 

##### Script to test run the commands for CAFA Toolset
The commands in this help file can be found in the script example.sh. One can
test the commands for this toolset by executing the following script at a
linux prompt.

```
sh example.sh > example.out.txt
```

The details of the usage description of the CAFA Toolset are as follows. 

### Integrating Annotation Datasets
This tool integrates protein annoations from multiple sources. Currently, it
supports two file formats: UniProtKB/SwissProt and UniProt-GOA. Here is the
command to run this tool:

```
python Mergedb -I1=uniprot_sprot.dat.2014_09 -I2=gene_association.goa_ref_yeast.38 -G 559292
```

The first input, uniprot_sprot.dat.2014_09, is the filename of a 
UniProtKB/SwissProt file. The second input, 
gene_association.goa_ref_yeast.38, is the filename of a UniProt-GOA file. 
The third input is the taxonomy id for which the records will be integrated 
together.

This command will extract the annotations for taxonomy id 559292 from the
UniProtKB/SwissProt file and append them at the end of the UniProt-GOA file,
considering only the entries that are NOT in the latter file.
It will create a new file with the combined data:
```
   gene_association.goa_ref_yeast.38+sprot.2014_09.1
```
whose file format would be the same as the UniProt-GOA format i.e. either
GAF 1.0 or GAF 2.0.

Multiple runs of this program with the same input arguments will create
subsequent versions of the output file where the file name will end with
subsequent version number, such as 2, 3, 4, etc.

##### Note 
The UniProtKB/SwissProt file uniprot_sprot.dat.38 is not uploaded to GitHub
as one of the example input files because of its large size. To retreive 
this specific file from the UniProt repository, please perform the following
commands:

```
wget ftp://ftp.uniprot.org/pub/databases/uniprot/previous_releases/release-2014_09/knowledgebase/uniprot_sprot-only2014_09.tar.gz
gzip -d uniprot_sprot-only2014_09.tar.gz
tar xvf uniprot_sprot-only2014_09.tar 
gzip -d uniprot_sprot.dat.gz
mv uniprot_sprot.dat uniprot_sprot.dat.2014_09
```

### Target Generation
This tool will create a file for the target set, containing the protein
sequences in the fasta file format. The simplest way to run the program 
for target generation:

```
python Filter -I1=uniprot_sprot.dat.2014_09 -G=559292
```
The first input is a UniProtKB/SwissProt annotation filename. The second 
input is the taxonomy id for the species (in this case Saccharomyces 
cerevisiae) whose protein sequences are being filtered. 

Successful run of this program will create the following two output files - 
one for the target sequences and one for the target id and protein name 
mapping used in the target sequence output file: 
uniprot_sprot.dat.2014_09.559292.tfa.1 and 
uniprot_sprot.dat.2014_09.559292.tfa.1.map, respectively.

* The target sequence output file name is created by adding an extension with
the name of the input file where the extension is formed in the following way:
[taxon id].[tfa].[version #].

* The map file name is created by adding '.map' at the end of the target sequence
output file name: [taxon id].[tfa].[version #].map

* Multiple runs of this program with the same input file will create
subsequent versions of the output files.

The program can also take an output filename to save the filtered sequences 
as a command line argument:

```
python Filter -I1=uniprot_sprot.dat.2014_09 -G=559292 -O=uniprot_sprot.dat.2014_09.559292.tfa
```

### Benchmark Creation
This tool will create benchmark files from two input annotation files in
UniProt-GOA file format at time points t1 and t2, respectively. The simplest
way to run this program:

```
python Benchmark -I1=gene_association.goa_ref_yeast.23 -I2=gene_association.goa_ref_yeast.52
```

The first input file, gene_association.goa_ref_yeast.23, is an annotation
file at time point t1 and the second input file,
gene_association.goa_ref_yeast.52, is an annotation file at time point t2.
Each of the input files must be in GAF 1.0 or GAF 2.0 format.

Execution of this program will create six benchmark files:

1. gene_association.goa_ref_yeast.52-23.benchmark_LK_mfo.1
2. gene_association.goa_ref_yeast.52-23.benchmark_LK_bpo.1
3. gene_association.goa_ref_yeast.52-23.benchmark_LK_cco.1
4. gene_association.goa_ref_yeast.52-23.benchmark_NK_mfo.1
5. gene_association.goa_ref_yeast.52-23.benchmark_NK_bpo.1
6. gene_association.goa_ref_yeast.52-23.benchmark_NK_cco.1

Files (1) – (3) are the three LK-benchmark files in MFO, BPO, and CCO 
categories, respectively. Files (4) – (6) are the three NK-benchmark 
files in these ontologies (MFO, BPO, and CCO), respectively. Running this 
tool multiple times with the same input file name at time point t2, will 
create the benchmark files that end with the subseqent version number, 
such as 2, 3, 4 etc.

### Benchmark Verification
This tool will verify the benchmark files generated by the Benchmark Creation 
tool. The simplest way to run the program:

```
python Verify -I1=gene_association.goa_ref_yeast.23 -I2=gene_association.goa_ref_yeast.52 -I3=gene_association.goa_ref_yeast.52-23.benchmark_LK_bpo.1
```

The first and the second input files are the two annotation files at time 
points t1 and t2, respectively. Each of the input files must be in GAF 1.0 
or GAF 2.0 format. The third input file, 
gene_association.goa_ref_yeast.52-23.benchmark_LK_bpo.1, is one of the 
benchmark files created by Benchmark Creation Tool. The program will find all 
the other benchmark files of the same version and verify the content in each 
of them for the correctness of the benchmark entries.

You must also supply all the optional parameters that you supplied while running 
the Benchmark Creation program to create this version of the benchmark files. 
This will verify all SIX benchmark files that end with .1, i.e dot one.

### Source Code
This is an open source project and the source code is publicly available on 
GitHub through the following URL: https://github.com/arkatebi/CAFA-Toolset.
For questions, please email either of us: Iddo Friedberg (idoerg@gmail.com),  
Ataur Katebi (arkatebi@gmail.com).

### References
[1] Radivojac P, Clark WT, Oron TR, et al. (2013). A large-scale evaluation of 
computational protein function prediction, Nature Methods 10(3), pp 221-227, 
PMID 23353650.
