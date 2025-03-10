#!/bin/bash
#SBATCH -J bloc-cnn-classifier       # Job name
#SBATCH --output=/sciclone/data10/iahewababarand/Deep_Learning_Project/classifiers/current/bloc-cnn-classifier-output.log        # Output file
#SBATCH --error=/sciclone/data10/iahewababarand/Deep_Learning_Project/classifiers/current/bloc-cnn-classifier-error.log       # Error file
#SBATCH -N 1                   # Number of nodes
#SBATCH -n 1                   # Number of tasks/cores per node
#SBATCH --gres=gpu:1           # Request 1 GPU
#SBATCH -t 48:00:00            # Runtime in hh:mm:ss
#SBATCH --mem=50G

python run_notebook.py > outputs.txt
