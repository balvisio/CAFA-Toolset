#~/bin/bash 
# This script will download the records for a list of proteins
# from uniprot database.
# Run this script with two arguments: 
# 1st argument: a file containing a list of proteins
# 2nd argument: an output file name 
# how to run: ./dl_cafa3targets.sh cafa3targetlist-uniq.csv cafa3targets_sprot.dat 
outfile=$2
nrows=$(cat "$1" | wc -l)
cat "$@"| 
{
while read name 
do 
 protName=$(echo $name | tr -d '\r')
 main_url="http://www.uniprot.org/uniprot/" 
 dl_url=$main_url$protName".txt"
 wget $dl_url
 fname=$protName".txt"
 cat $fname >> $outfile
 rm $fname
 #break
done 
}
echo "Done"
