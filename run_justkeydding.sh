#!/bin/bash

echo $1
echo "file	output" > $1_justkeydding.tsv
for f in $(ls $1 | grep ".krn")
do
	echo $f
	output=$(python3 -m justkeydding --majorEmission simple_harmonic_minor --minorEmission simple_harmonic_minor --transition ktg_exponential15 --json $1/$f)
	echo "$f	$output" >> $1_justkeydding.tsv
done
