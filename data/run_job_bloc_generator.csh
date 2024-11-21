#!/bin/bash
#SBATCH -J bloc-cnn       # Job name
#SBATCH --output=/sciclone/data10/iahewababarand/bloc-cnn/logs/bloc-cnn-output.log        # Output file
#SBATCH --error=/sciclone/data10/iahewababarand/bloc-cnn/logs/bloc-cnn-error.log       # Error file
#SBATCH -N 1                   # Number of nodes
#SBATCH -n 1                   # Number of tasks/cores per node
#SBATCH --gres=gpu:1           # Request 1 GPU
#SBATCH -t 24:00:00              # Runtime in hh:mm:ss
#SBATCH --mem=20G

python ./data/bloc_processor.py > ./logs/outputs.txt
