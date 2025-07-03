#!/bin/bash

#SBATCH -J SpMV
#SBATCH -o log/out-%j.log
#SBATCH -e error/out-%j.err
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -c 72
#SBATCH -p gpu
#SBATCH -t 10:00:00

module load vtune/2025.0.0
module load python/3.10.6

srun python3 principal.py spmv --outputdir 27-06-spmv
#srun python3 principal.py bfs --outputdir 29-05-bfs
#srun python3 principal.py cfd --outputdir 29-05-cfd
#srun python3 principal.py hotspot --outputdir 30-04-hotspot
#srun python3 principal.py lavaMD --outputdir 30-04-lavaMD
#srun python3 principal.py gemm --outputdir 30-04-gemm
#srun python3 principal.py jacobi2d --outputdir 30-04-jacobi2d
#srun python3 principal.py backprop --outputdir 29-05-backprop
#srun python3 principal.py convolution3d --outputdir 06-05-convolution3d
