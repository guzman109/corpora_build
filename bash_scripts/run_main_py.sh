#!/bin/bash

# Change to directory with test data
PY_SCRIPT="/home/gdbartlettclab/cxg078/Documents/corpora_build/python_scripts/main.py"
	
# Search for .tex files in test_data directory and add to an array.
TEX_FILES=$(find "$1/$2" -name "*.tex")
TEX_FILES=${TEX_FILES[0]}
IFS=$'\n' read -rd '' -a TEX_FILES<<<"$TEX_FILES"
IFS=$'\n' TEX_FILES=($(sort <<<"${TEX_FILES[*]}")); unset IFS

echo "In Script"

# Iterates through .tex fiels and send them to python script
# Right now I'm skipping files that are examples since they crashed the python script.
i=0
for f in "${TEX_FILES[@]}"; do
	if echo "$f" | grep -iqFv 'example' ; then
		echo "Starting python script with $f"
		python3 "$PY_SCRIPT" "$f" $2 $i $3
		((i++))
	fi
done

echo "Exiting Script"

