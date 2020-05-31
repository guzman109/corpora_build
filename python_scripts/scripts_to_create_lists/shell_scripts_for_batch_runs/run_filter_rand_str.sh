#!/bin/bash
#SBATCH --partition=himem
#SBATCH -n 1
#SBATCH -c 1
#SBATCH --mem=500G

module load python/3.7.3
python filter_rand_str.py $1 $2
