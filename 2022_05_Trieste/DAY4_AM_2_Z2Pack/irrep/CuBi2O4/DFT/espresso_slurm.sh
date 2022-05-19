#!/bin/bash                                                          
#SBATCH --partition=regular
#SBATCH --job-name=cu
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --time=24:00:00
#SBATCH --mem=12GB
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err
#SBATCH --mail-user=mikeliraola95@gmail.com
#SBATCH --mail-type=FAIL

module load QuantumESPRESSO/6.4-intel-2018a


export NPROCS=$SLURM_CPUS_PER_TASK
export WORK_DIR=/scratch/$USER/jobs/$SLURM_JOBID
export OUT_DIR=$WORK_DIR/out
export PSEUDO_DIR=$WORK_DIR/pseudo
mkdir -p $WORK_DIR
mkdir -p $OUT_DIR

# Generate input files for Quantum Espresso calculation
cp -r $SLURM_SUBMIT_DIR/generate_input_espresso.sh $WORK_DIR 
cp -r $SLURM_SUBMIT_DIR/pseudo $WORK_DIR 
cd $WORK_DIR
bash generate_input_espresso.sh

# SELF-CONSISTENT calculation
mkdir $WORK_DIR/scf
cp $WORK_DIR/scf.in $WORK_DIR/scf
cd $WORK_DIR/scf
srun pw.x < scf.in > scf.out
cp -r $WORK_DIR/scf $SLURM_SUBMIT_DIR
cd $WORK_DIR

## calculate WAVE-FUNCTIONS for IrRep
#mkdir $WORK_DIR/IrRep
#cp $WORK_DIR/scf_IrRep.in $WORK_DIR/IrRep
#cd $WORK_DIR/IrRep
#srun pw.x < scf_IrRep.in > scf_IrRep.out
#cp -r $WORK_DIR/IrRep $SLURM_SUBMIT_DIR
#cd $WORK_DIR

# BANDS calculation
mkdir $WORK_DIR/bands
cp $WORK_DIR/bands.in $WORK_DIR/bands
cp $WORK_DIR/pp.bands.in $WORK_DIR/bands
cd $WORK_DIR/bands
srun pw.x < bands.in > bands.out
srun bands.x < pp.bands.in > pp.bands.out
cp -r $WORK_DIR/bands $SLURM_SUBMIT_DIR
cd $WORK_DIR

cp -r $OUT_DIR $SLURM_SUBMIT_DIR
cd $SLURM_SUBMIT_DIR
rm -rf $WORK_DIR
