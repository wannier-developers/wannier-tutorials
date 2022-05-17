#!/bin/bash
#SBATCH --job-name Fe
#SBATCH --mail-type=none
#SBATCH -N 1
#SBATCH -n 8
#SBATCH -p cmt
#SBATCH --mem=120g
#SBATCH -t 0-20:00:00
#SBATCH -e slurm-out.txt
#SBATCH -o slurm-out.txt
#SBATCH --mail-user=stepan@physik.uzh.ch

export NSLOTS=8 # $(wc -l $PBS_NODEFILE | awk '{print $1}')

export OMP_NUM_THREADS=1


ln -s ../input/* .
source /app/physik/intel/2018.4/parallel_studio_xe_2018.4.057/psxevars.sh intel64


wanpath="/home/fkp/stepan/data11/wannier90-versions/wannier90-save4wberri"
export QEPATH="/app/theorie/qe-6.4.1/bin"
qerun="mpirun -np $NSLOTS  $QEPATH/pw.x -nk $NSLOTS " 
bands="$QEPATH/bands.x -mk $NSLOTS " 
pw2wan="mpirun -np $NSLOTS  $QEPATH/pw2wannier90.x " 
wan="mpirun -np $NSLOTS $wanpath/wannier90.x"
wan_serial="$wanpath/wannier90.x"
postw90="mpirun -np $NSLOTS $wanpath/post90.x"


echo "SCF calculation"
time $qerun < Fe_pw_scf_in > Fe_pw_scf_out
echo "bands calculation"
time $qerun < Fe_pw_bands_in > Fe_pw_bands_out
time $bands < Fe_bandsX_in > Fe_bandsX_out
mv bands.out.gnu Fe_bands_pw.dat
echo "NSCF calculation"
time $qerun < Fe_pw_nscf_in > Fe_pw_nscf_out
echo "pw2wannier90 calculation"
time $wan_serial -pp Fe
time $pw2wan < Fe_pw2wan_in > Fe_pw2wan_out
echo "wannnierization"
time $wan Fe
gnuplot Fe_band_pw+wan.gnu
echo "pw2wannier uHu"
time $pw2wan < Fe_pw2wan_uHu_in > Fe_pw2wan_uHu_out
