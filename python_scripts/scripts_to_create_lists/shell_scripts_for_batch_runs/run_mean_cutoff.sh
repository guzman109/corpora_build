#!/bin/bash
#SBATCH --partition=himem
#SBATCH -n 1
#SBATCH -c 2
#SBATCH --mem=250G
module load python/3.7.3

python mean_cutoff.py $1
