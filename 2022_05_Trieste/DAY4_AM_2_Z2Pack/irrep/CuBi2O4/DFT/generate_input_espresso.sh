# SCF input file for Quantum Espresso
cat > scf.in << EOF
&CONTROL
   calculation     =  'scf',
   prefix          =  'cubi2o4',
   pseudo_dir = '$PSEUDO_DIR',
   outdir='$OUT_DIR',
   restart_mode    =  'from_scratch',
   disk_io         = 'nowf',
   verbosity       = 'high'
 /

 &SYSTEM
   ibrav           =  0,
   A               =  1.0,
   degauss         =  0.001,
   ecutwfc         =  33.09,
   nat             =  28,
   ntyp            =  3,
   occupations     =  'smearing',
   smearing        =  'mp',
   lspinorb        = .False.
   noncolin        = .False.
 /

 &ELECTRONS
   mixing_beta = 0.7,
   conv_thr    = 1e-8,
 /

CELL_PARAMETERS alat
8.475000000   0.000000000   0.000000000                                      
0.000000000   8.475000000   0.000000000                                      
0.000000000   0.000000000   5.806000000

ATOMIC_SPECIES
  O  16  O.UPF
  Bi 209 Bi.UPF
  Cu 64  Cu.UPF

ATOMIC_POSITIONS crystal
O  0.049   0.141   0.089 
O  0.451   0.359   0.089 
O  0.359   0.049   0.089 
O  0.141   0.451   0.089
O  0.951   0.641   0.411 
O  0.549   0.859   0.411 
O  0.641   0.549   0.411 
O  0.859   0.951   0.411
O  0.951   0.859   0.911 
O  0.549   0.641   0.911 
O  0.641   0.951   0.911 
O  0.859   0.549   0.911 
O  0.049   0.359   0.589 
O  0.451   0.141   0.589 
O  0.359   0.451   0.589 
O  0.141   0.049   0.589
Bi  0.418   0.582   0.250
Bi  0.082   0.918   0.250
Bi  0.918   0.418   0.250 
Bi  0.582   0.082   0.250
Bi  0.582   0.418   0.750
Bi  0.918   0.082   0.750
Bi  0.082   0.582   0.750
Bi  0.418   0.918   0.750
Cu  0.250   0.250   0.078
Cu  0.750   0.750   0.422
Cu  0.750   0.750   0.922
Cu  0.250   0.250   0.578

K_POINTS automatic
  9   9   11   0   0   0
EOF

# SCF at MAXIMAL K-POINTS input file for Quantum Espresso
#cat > scf_IrRep.in << EOF
#&CONTROL
#   calculation     =  'scf',
#   prefix          =  'bi2se3',
#   pseudo_dir = '$PSEUDO_DIR',
#   outdir='$OUT_DIR',
#   restart_mode    =  'from_scratch',
#   disk_io         = 'medium'
# /
#
# &SYSTEM
#   ibrav           =  0,
#   A               =  1.0,
#   degauss         =  0.0001,
#   ecutwfc         =  33.09,
#   nat             =  2,
#   ntyp            =  3,
#   occupations     =  'smearing',
#   smearing        =  'mv',
#   lspinorb        = .TRUE.
#   noncolin        = .TRUE.
# /
#
# &ELECTRONS
#   startingpot = file
#   mixing_beta = 0.3,
#   conv_thr    = 1e-8,
# /
#
#CELL_PARAMETERS alat
#     2.0714999999999995    1.1959810826263095    9.5453333333333319
#    -2.0714999999999995    1.1959810826263095    9.5453333333333319
#     0.0000000000000000   -2.3919621652526191    9.5453333333333319
#
#ATOMIC_SPECIES
#  Bi 209  Bi.upf
#  Se 79   Se.upf
#
#ATOMIC_POSITIONS crystal
#Bi  0.6014999999999998  0.6014999999999999  0.6014999999999999
#Bi  0.3985000000000000  0.3985000000000001  0.3984999999999999
#Se  0.0000000000000000  0.0000000000000000  0.0000000000000000
#Se  0.7885000000000000  0.7885000000000000  0.7885000000000000
#Se  0.2114999999999999  0.2114999999999999  0.2114999999999999
#
#K_POINTS crystal
#4
#0.00    0.00    0.00    1.0
#0.50    0.50    0.50    1.0 
#0.50    0.50    0.00    1.0
#0.00    0.50    0.00    1.0
#EOF

# BANDS input file for Quantum Espresso
cat > bands.in << EOF
&CONTROL
   calculation     =  'bands',
   prefix          =  'cubi2o4',
   pseudo_dir = '$PSEUDO_DIR',
   outdir='$OUT_DIR',
   restart_mode    =  'from_scratch',
   disk_io         = 'medium',
   verbosity       = 'high'
 /

 &SYSTEM
   ibrav           =  0,
   A               =  1.0,
   degauss         =  0.001,
   ecutwfc         =  33.09,
   nat             =  28,
   ntyp            =  3,
   occupations     =  'smearing',
   smearing        =  'mp',
   lspinorb        = .False.
   noncolin        = .False.
 /

 &ELECTRONS
   mixing_beta = 0.7,
   conv_thr    = 1e-8,
 /

CELL_PARAMETERS alat
8.475000000   0.000000000   0.000000000                                      
0.000000000   8.475000000   0.000000000                                      
0.000000000   0.000000000   5.806000000

ATOMIC_SPECIES
  O  16  O.UPF
  Bi 209 Bi.UPF
  Cu 64  Cu.UPF

ATOMIC_POSITIONS crystal
O  0.049   0.141   0.089 
O  0.451   0.359   0.089 
O  0.359   0.049   0.089 
O  0.141   0.451   0.089
O  0.951   0.641   0.411 
O  0.549   0.859   0.411 
O  0.641   0.549   0.411 
O  0.859   0.951   0.411
O  0.951   0.859   0.911 
O  0.549   0.641   0.911 
O  0.641   0.951   0.911 
O  0.859   0.549   0.911 
O  0.049   0.359   0.589 
O  0.451   0.141   0.589 
O  0.359   0.451   0.589 
O  0.141   0.049   0.589
Bi  0.418   0.582   0.250
Bi  0.082   0.918   0.250
Bi  0.918   0.418   0.250 
Bi  0.582   0.082   0.250
Bi  0.582   0.418   0.750
Bi  0.918   0.082   0.750
Bi  0.082   0.582   0.750
Bi  0.418   0.918   0.750
Cu  0.250   0.250   0.078
Cu  0.750   0.750   0.422
Cu  0.750   0.750   0.922
Cu  0.250   0.250   0.578

K_POINTS crystal_b
2
0.00 0.00 0.00 30 ! G
0.00 0.50 0.00 30 ! X
EOF

# post-processing of bands with bands.x
cat > pp.bands.in << EOF
&bands
   outdir='$OUT_DIR',
   prefix          =  'cubi2o4',
   filband         = 'cubi2o4.bands.dat'
/
EOF
