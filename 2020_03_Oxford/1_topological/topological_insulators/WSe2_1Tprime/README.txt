# Study topological properties of 1T'-WSe2

1. Preparation: First, please copy the tutorial input files of the exercise

   $ git clone https://github.com/wannier-developers/wannier-tutorials.git
   $ cd wannier-tutorials/2020_03_Oxford/1_topological/topological_insulators/WSe2_1Tprime/
   $ tar xzvf wannier90_hr.dat.tar.gz

2. Run WannierTools:

   $ mpirun -np 2 wt.x &

3. Visualize the results using Gnuplot

   $ gnuplot bulkek.gnu
   $ gnuplot wcc.gnu
   $ gnuplot surfdos_l.gnu
   $ gnuplot surfdos_r.gnu
