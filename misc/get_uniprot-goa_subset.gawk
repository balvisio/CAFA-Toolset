#!/bin/awk -f
# How to run this script: 
# gawk -f get_uniprot-goa_subset.gawk file1 file2
# the script will compare the column 1 of file1 with 
# the column 2 of file2. 
# If there is a match, it will output the corresponding 
# line from file2.

BEGIN {
    FS="\t";
}
{
    if (FNR==NR){
       tmp=substr($0,1,length($0)-1) # Remove the end of line character 
       a[tmp]=tmp;
       #a[$1]=$1; 
       next;
    }
    if ($2 in a){
       #print $2
       print $0
    }
}

END {
    ;
}
