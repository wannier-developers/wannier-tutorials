# SCF input file for Quantum Espresso
cat > scf.in << EOF
&CONTROL
   calculation     =  'scf',
   prefix          =  'snte',
   pseudo_dir = '$PSEUDO_DIR',
   outdir='$OUT_DIR',
   restart_mode    =  'from_scratch',
 /

 &SYSTEM
   ibrav           =  0,
   A               =  6.309,
   degauss         =  0.0001,
   ecutwfc         =  33.09,
   nat             =  2,
   ntyp            =  2,
   occupations     =  'smearing',
   smearing        =  'mv',
 /

 &ELECTRONS
   mixing_beta = 0.3,
   conv_thr    = 1e-8,
 /

CELL_PARAMETERS alat
  0.0000000000000000   0.5000000000000000   0.5000000000000000   
  0.5000000000000000   0.0000000000000000   0.5000000000000000
  0.5000000000000000   0.5000000000000000   0.0000000000000000

ATOMIC_SPECIES
  Sn 118   Sn.upf
  Te 128   Te.upf

ATOMIC_POSITIONS crystal
Sn             0.0000000000        0.0000000000        0.0000000000
Te             0.5000000000        0.5000000000        0.5000000000

K_POINTS automatic
  5   5   5   0   0   0
EOF

# SCF at MAXIMAL K-POINTS input file for Quantum Espresso
cat > scf_IrRep.in << EOF
&CONTROL
   calculation     =  'scf',
   prefix          =  'snte',
   pseudo_dir = '$PSEUDO_DIR',
   outdir='$OUT_DIR',
   restart_mode    =  'from_scratch',
 /

 &SYSTEM
   ibrav           =  0,
   A               =  6.309,
   degauss         =  0.0001,
   ecutwfc         =  33.09,
   nat             =  2,
   ntyp            =  2,
   occupations     =  'smearing',
   smearing        =  'mv',
 /

 &ELECTRONS
   startingpot = file
   mixing_beta = 0.3,
   conv_thr    = 1e-8,
 /

CELL_PARAMETERS alat
  0.0000000000000000   0.5000000000000000   0.5000000000000000   
  0.5000000000000000   0.0000000000000000   0.5000000000000000
  0.5000000000000000   0.5000000000000000   0.0000000000000000

ATOMIC_SPECIES
  Sn 118   Sn.upf
  Te 128   Te.upf

ATOMIC_POSITIONS crystal
Sn             0.0000000000        0.0000000000        0.0000000000
Te             0.5000000000        0.5000000000        0.5000000000

K_POINTS crystal
5
0.00    0.00    0.00    1.0
0.50    0.00    0.50    1.0 
0.50    0.50    0.50    1.0
0.50    0.25    0.75    1.0
EOF

# BANDS input file for Quantum Espresso
cat > bands.in << EOF
&CONTROL
   calculation     =  'bands',
   prefix          =  'snte',
   pseudo_dir = '$PSEUDO_DIR',
   outdir='$OUT_DIR',
   restart_mode    =  'from_scratch',
 /

 &SYSTEM
   ibrav           =  0,
   A               =  6.309,
   degauss         =  0.0001,
   ecutwfc         =  33.09,
   nat             =  2,
   ntyp            =  2,
   occupations     =  'smearing',
   smearing        =  'mv',
 /

 &ELECTRONS
   mixing_beta = 0.3,
   conv_thr    = 1e-8,
 /

CELL_PARAMETERS alat
  0.0000000000000000   0.5000000000000000   0.5000000000000000   
  0.5000000000000000   0.0000000000000000   0.5000000000000000
  0.5000000000000000   0.5000000000000000   0.0000000000000000

ATOMIC_SPECIES
  Sn 118   Sn.upf
  Te 128   Te.upf

ATOMIC_POSITIONS crystal
Sn             0.0000000000        0.0000000000        0.0000000000
Te             0.5000000000        0.5000000000        0.5000000000

K_POINTS crystal_b
4
0.50 0.00 0.50 30 ! X
0.50 0.25 0.75 30 ! W
0.50 0.50 0.50 30 ! L
0.00 0.00 0.00 30 ! G
0.50 0.00 0.50 30 ! X
EOF

# POST-PROCESSING bands with bands.x
cat > pp.bands.in << EOF
&bands
   outdir='$OUT_DIR',
   prefix          =  'snte',
   filband         = 'snte.bands.dat'
/
EOF

