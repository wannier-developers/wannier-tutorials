#!/usr/bin/env python3


## these linesline if you want to use the git version of the code, instead of the one installed by pip
num_proc=32

import wannierberri as wberri

import numpy as np


SYM=wberri.symmetry

Efermi=np.linspace(12.,13.,1001)
system=wberri.System(tb_file='Fe_tb.dat',getAA=True)
#generators=[]

wberri.integrate(system,
            NK=100,
            Efermi=Efermi, 
            smearEf=10,
            quantities=["ahc","cumdos"],
            numproc=num_proc,
            adpt_num_iter=5,
            fout_name='Fe_R_sym',
            symmetry_gen=generators,
            restart=False,
            )


system=wberri.System(seedname='Fe',getAA=True,
               getCC=True,   #  needed for orbital moment
               getSS=True    #  needed for spin
                   )
generators=[SYM.Inversion,SYM.C4z,SYM.TimeReversal*SYM.C2x]



wberri.integrate(system,
            NK=200,
            Efermi=Efermi, 
            smearEf=10,
            quantities=["ahc","Morb","spin""],
            numproc=num_proc,
            adpt_num_iter=5,
            fout_name='Fe_R_sym',
            symmetry_gen=generators,
            restart=False,
            )



if False:
  wberri.tabulate(system,
             NK=100,
             quantities=["berry","morb","spin"],
             symmetry_gen=generators,
             fout_name='Fe',
             numproc=num_proc,
             ibands=np.arange(4,10),
             Ef0=12.6)
