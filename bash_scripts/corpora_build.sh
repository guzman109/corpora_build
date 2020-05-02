#!/bin/bash
#SBATCH --job-name=corpora_build
#SBATCH --nodes=15

## Extracts all .gz files within the arXiv tar files
extract_inner_directories(){
	#Search for .gz files and add to array
	FILES=$(find "$1" -name '*.gz')
	FILES=${FILES[0]}
	IFS=$'\n' read -rd '' -a FILES<<<"$FILES"; unset IFS
	IFS=$'\n' FILES=($(sort <<<"${FILES[*]}")); unset IFS
	cd * 

	#Extract files into proper directories.
	for f in "${FILES[@]}"; do
		DIR="$(echo "$f" | perl -pe "s/.*[0-9]{4}\///g and s/.gz//g")"	

		# Create directories to extract each .gz file
		mkdir "$DIR"
		mv "$f" "$DIR"
		cd "$DIR/"
		
		#echo "Extracting Files in $DIR"
		gunzip * && tar xf * 2>/dev/null && rm $DIR
		DID_NOT_EXTRACT=$(find * -name "$DIR")
		if [ ${#DID_NOT_EXTRACT} -ne 0 ]; then
			FILE=$(file * | grep -Eo ' LaTeX | TeX | ASCII ')
			if [ ${#FILE} -ne 0 ] ; then
				mv "$DIR" "$DIR".tex
			fi
		fi
		cd ..
	done
}

## Create the arXiv directory in the test_data directory and begin extracting tar file and call
##  extract_inner_directories to extract all .gz files contained in arXiv directory.
create_directory(){
# Find unique name of arXiv folder and create a new (temporary) directory 
#  to copy the .tar file. Extract the .tar file afterwards.
	TEMP=$(echo $1 | grep -Eo 'arXiv_src_[0-9]{4}_[0-9]{3}')
	TAR_NAME=$TEMP

	## Create directories in the results directory to organize results from each arXiv
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/$TEMP"
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/$TEMP/C_lists"
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/$TEMP/Q_lists"
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/$TEMP/QC_lists"
	
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/$TEMP/C_lists/C1_lists"
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/$TEMP/C_lists/C2_lists"
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/$TEMP/C_lists/C3_lists"

	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/$TEMP/Q_lists/Q1_lists"
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/$TEMP/Q_lists/Q2_lists"
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/$TEMP/Q_lists/Q3_lists"
	
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/$TEMP/QC_lists/QC1_lists"
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/$TEMP/QC_lists/QC2_lists"
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/$TEMP/QC_lists/QC3_lists"

	# Make directory and copy file
	mkdir "$2/$TEMP"
	cp $1 "$2/$TEMP"
	cd "$2/$TEMP"

	# Time to extract
	echo "Extracting Files in $TEMP"
	tar -xf "$TEMP".tar 
		
	# Extract inner directories
	extract_inner_directories "$2/$TEMP"	
}

## Change the encoding of files to 'utf-8' if possible.
change_encoding() { 
# Search for .tex files in test_data directory and add to an array.
	TEX_FILES=$(find "$1" -name "*.tex")
	TEX_FILES=${TEX_FILES[0]}
	IFS=$'\n' read -rd '' -a TEX_FILES<<<"$TEX_FILES"

  # Iterates through .tex files and changes the encoding from iso-8859-1 to utf-8.
  # This is done in order for the python script to open and recognize the file.
	for f in "${TEX_FILES[@]}"; do
		str=$(echo "$(file -i "$f")" | awk 'BEGIN{FS="="}{print $2}')
  # Delete files that have an unknown encoding. (Cannot be changed to utf-8).
		if [ "$str" == "unknown-8bit" ] || [ "$str" == "binary" ] ; then
 			rm "$f"
		fi
	done

# Search for .tex files in test_data directory and add to an array.
	TEX_FILES=$(find "$1" -name "*.tex")
	TEX_FILES=${TEX_FILES[0]}
	IFS=$'\n' read -rd '' -a TEX_FILES<<<"$TEX_FILES"

	for f in "${TEX_FILES[@]}"; do
		str=$(echo "$(file -i "$f")" | awk 'BEGIN{FS="="}{print $2}')
		if [ "$str" != "utf-8" ] ; then
			iconv -f "$str" -t "utf-8" "$f" > "${f}.utf" &&
			mv -f "${f}.utf" "$f"
		fi
	done
}

main() {
	## Load python 3.7.3 and set up nltk
	module load python/3.7.3
	python3 "/home/gdbartlettclab/cxg078/Documents/corpora_build/python_scripts/nltk_setup.py"

	## Paths to orginal arXiv_files, test_data, main.py, slurm_files(output from srun)
	PATH_TAR='/home/gdbartlettclab/lab/arXiv_files'
	PATH_TAR_COPY='/home/gdbartlettclab/cxg078/Documents/corpora_build/test_data'
	PATH_TO_RUN_PY='/home/gdbartlettclab/cxg078/Documents/corpora_build/bash_scripts/run_main_py.sh'
	FILE_OUTPUT='/home/gdbartlettclab/cxg078/Documents/corpora_build/slurm_files'

	## Global variable to hold current arXiv folder. Used to organize results.
	TAR_NAME=''
	
	## Grab all arXiv file names
	TAR_FILE_ARRAY=$(find "$PATH_TAR" -name '*.tar')
	TAR_FILE_ARRAY=${TAR_FILE_ARRAY[0]}
	IFS=$'\n' read -rd '' -a TAR_FILE_ARRAY<<<"$TAR_FILE_ARRAY"; unset IFS
	IFS=$'\n' TAR_FILE_ARRAY=($(sort <<<"${TAR_FILE_ARRAY[*]}")); unset IFS	
	
	j=1 ##Used to keep track of the number of srun processes running.
	for f in "${TAR_FILE_ARRAY[@]}"; do
		## Extract files and change encoding of tex files to utf-8
		create_directory $f $PATH_TAR_COPY
		change_encoding $PATH_TAR_COPY/$TAR_NAME
		
		## Create output file for each srun node and call srun.
		touch "$FILE_OUTPUT/node$j.txt"
		echo "Starting Node $J"
		srun -N 1 --output="$FILE_OUTPUT/node$j.txt" bash $PATH_TO_RUN_PY $PATH_TAR_COPY $TAR_NAME &
		
		## Wait if all nodes are currently used up. Then delete current test_data folder to save space.
		if [ $(($j%15)) -eq 0 ]; then
			echo "Waiting..."
			wait
			cd "$PATH_TAR_COPY"
			rm -r *
		fi
		((j++))
	done
}

main
