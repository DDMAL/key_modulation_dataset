#!/bin/bash

mkdir all_files
for f in $(find . | grep ".krn")
do
	echo $f
	cp $f all_files/
done
