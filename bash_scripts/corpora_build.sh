#!/bin/bash
#SBATCH --job-name=corpora_build
#SBATCH --nodes=1
#SBATCH --ntasks=10

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
		cd "$DIR"
		
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
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/node$3/$TEMP"
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/node$3/$TEMP/C_lists"
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/node$3/$TEMP/Q_lists"
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/node$3/$TEMP/QC_lists"
	
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/node$3/$TEMP/C_lists/C1_lists"
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/node$3/$TEMP/C_lists/C2_lists"
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/node$3/$TEMP/C_lists/C3_lists"

	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/node$3/$TEMP/Q_lists/Q1_lists"
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/node$3/$TEMP/Q_lists/Q2_lists"
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/node$3/$TEMP/Q_lists/Q3_lists"
	
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/node$3/$TEMP/QC_lists/QC1_lists"
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/node$3/$TEMP/QC_lists/QC2_lists"
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/node$3/$TEMP/QC_lists/QC3_lists"

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
		if [ "$str" == "iso-8859-1" ] ; then
			iconv -f "$str" -t "utf-8" "$f" > "${f}.utf" &&
			mv -f "${f}.utf" "$f"
		fi
	done

	## Delete files that have an unknown encoding. (Cannot be changed to utf-8).	
	#for f in "${TEX_FILES[@]}"; do
	#	str=$(echo "$(file -i "$f")" | awk 'BEGIN{FS="="}{print $2}')
	#	if [ "$str" != "utf-8" ] ; then
 	#		rm "$f"
	#	fi
	#done

}

main() {
	## Load python 3.7.3 and set up nltk
	module load python/3.7.3
	python3 "/home/gdbartlettclab/cxg078/Documents/corpora_build/python_scripts/nltk_setup.py"

	## Paths to orginal arXiv_files, test_data, main.py, slurm_files(output from srun)
	PATH_TAR='/home/gdbartlettclab/lab/arXiv_files'
	PATH_TAR_COPY="/home/gdbartlettclab/cxg078/Documents/corpora_build/test_data/node$1"
	PATH_TO_RUN_PY='/home/gdbartlettclab/cxg078/Documents/corpora_build/bash_scripts/run_main_py.sh'
	FILE_OUTPUT="/home/gdbartlettclab/cxg078/Documents/corpora_build/slurm_files/node$1"

	## Global variable to hold current arXiv folder. Used to organize results.
	TAR_NAME=''

	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/results/node$1" 
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/test_data/node$1"
	mkdir "/home/gdbartlettclab/cxg078/Documents/corpora_build/slurm_files/node$1"
	
	## Grab all arXiv file names
	TAR_FILE_ARRAY=$(find "$PATH_TAR" -name '*.tar')
	TAR_FILE_ARRAY=${TAR_FILE_ARRAY[0]}
	IFS=$'\n' read -rd '' -a TAR_FILE_ARRAY<<<"$TAR_FILE_ARRAY"; unset IFS
	IFS=$'\n' TAR_FILE_ARRAY=($(sort <<<"${TAR_FILE_ARRAY[*]}")); unset IFS	
	
	j=0 ##Used to keep track of the number of srun processes running.
	k=0

  	val=$2
  	while [ $val -le $3 ]; do
    		ARR[${k}]=$val
  		((val++))
    		((k++))
  	done	

	k=0
	for i in ${ARR[*]}; do
		## Extract files and change encoding of tex files to utf-8
		create_directory ${TAR_FILE_ARRAY[$i]} $PATH_TAR_COPY $1
		change_encoding $PATH_TAR_COPY/$TAR_NAME
		
		## Create output file for each srun node and call srun.
		touch "$FILE_OUTPUT/$TAR_NAME.out"
		echo "Starting $TAR_NAME"
		srun -n 1 --output="$FILE_OUTPUT/$TAR_NAME.out" bash $PATH_TO_RUN_PY $PATH_TAR_COPY $TAR_NAME $1 &
		SRUN_PIDS[${j}]=$!
		## Wait if all nodes are currently used up. Then delete current test_data folder to save space.
		if [ $j -eq 19 ]; then
      			echo "Waiting for ${#SRUN_PIDS[@]} srun process currently running...."
      			for pid in ${SRUN_PIDS[*]}; do
        			time wait $pid
      			done
      			mkdir "$PATH_TAR_COPY/delete_$k"
      			mv "$PATH_TAR_COPY/"arX* "$PATH_TAR_COPY/delete_$k"
			mkdir "$PATH_TAR_COPY/empty$k"
      			rsync -a --delete "$PATH_TAR_COPY/empty$k/" "$PATH_TAR_COPY/delete_$k/" &
      			((k++))
      			j=0
		else
		  ((j++))
		fi
	done
	((k++))
	#Wait one final time to ensure all processes are done.
	echo "Waiting for ${#SRUN_PIDS[@]} srun process currently running...."
  	for pid in ${SRUN_PIDS[*]}; do
    		time wait $pid
  	done
  	mkdir "$PATH_TAR_COPY/delete_$k"
  	mv "$PATH_TAR_COPY/"arX* "$PATH_TAR_COPY/delete_$k"
	mkdir "$PATH_TAR_COPY/empty$k"
      	rsync -a --delete "$PATH_TAR_COPY/empty$k/" "$PATH_TAR_COPY/delete_$k/"
  	echo "Waiting for any process still running..."
  	time wait
}
## $1: node[1-5]
## $2: start of array
## $3: end of array
main $1 $2 $3
