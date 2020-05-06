#!/bin/bash

echo "file	output" > run_justkeydding.tsv
for f in $(ls all_files | grep ".krn")
do
	echo $f
	output=$(python3 -m justkeydding --json all_files/$f)
	echo "$f	$output" >> run_justkeydding.tsv
done
