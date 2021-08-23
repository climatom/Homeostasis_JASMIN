#!/bin/bash

# Params for sbatch
#SBATCH --partition=short-serial
#SBATCH --job-name=ssp_home
#SBATCH -o %j_ssp.out
#SBATCH -e %j_ssp.err
#SBATCH --time=06:00:00
#SBATCH --array=1-299

# Set environment 
module add jaspy
cd /home/users/tommatthews/Homeostasis/
source /home/users/tommatthews/Homeostasis/xheat/bin/activate

# Launch
python compute_ssp.py ${SLURM_ARRAY_TASK_ID}





