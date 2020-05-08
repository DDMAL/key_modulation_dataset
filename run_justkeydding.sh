#!/bin/bash

echo "file	output" > run_justkeydding.tsv
for f in $(ls all_files | grep ".krn")
do
	echo $f
	output=$(python3 -m justkeydding --majorEmission simple_harmonic_minor --minorEmission simple_harmonic_minor --transition ktg_exponential15 --json all_files/$f)
	echo "$f	$output" >> run_justkeydding.tsv
done
