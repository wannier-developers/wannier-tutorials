#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess

import z2pack
import matplotlib.pyplot as plt

##########################################################
############## Paths stuff ###############################
##########################################################
qedir = "/media/ictpuser/AiiDA/codes/QE_5_Z2pack/bin"
mpirun = "mpirun -np 4 "
pwcmd = mpirun + qedir + "/pw.x "
pw2wancmd = qedir + "/pw2z2pack.x "
z2cmd = pwcmd + "-inp snte.nscf.in >& pw.log;" + pw2wancmd + "-inp snte.pw2z2.in >& pw2z2.log;"
##########################################################
############## Paths stuff ###############################
##########################################################

##########################################################
############## SCF Calculation ###########################
##########################################################
# run the scf calculation
os.makedirs('scf', exist_ok=True)
if not os.path.isfile('./scf/SnTe.save/charge-density.dat'):
    print("Running the scf calculation")
    shutil.copy('input/snte.scf.in', 'scf')
    subprocess.check_output(
        pwcmd + " -inp snte.scf.in > scf.out", shell=True, cwd='scf'
    )
##########################################################
############## SCF Calculation ###########################
##########################################################

##########################################################
############## Defining Systems ##########################
##########################################################
# creating the z2pack.fp objects
snte_plus = z2pack.fp.System(
    input_files=[
        os.path.join('input', fn)
        for fn in ['snte.nscf.in', 'snte.pw2z2+i.in']
    ],
    file_names=["snte.nscf.in", "snte.pw2z2.in"],
    kpt_fct=[z2pack.fp.kpoint.qe],
    kpt_path=["snte.nscf.in"],
    command=z2cmd,
    executable='/bin/bash',
    mmn_path='snte.mmn'
)
snte_minus = z2pack.fp.System(
    input_files=[
        os.path.join('input', fn)
        for fn in ['snte.nscf.in', 'snte.pw2z2-i.in']
    ],
    file_names=["snte.nscf.in", "snte.pw2z2.in"],
    kpt_fct=[z2pack.fp.kpoint.qe],
    kpt_path=["snte.nscf.in"],
    command=z2cmd,
    executable='/bin/bash',
    mmn_path='snte.mmn'
)
##########################################################
############## Defining Systems ##########################
##########################################################

##########################################################
############## Defining Settings #########################
##########################################################
settings = {
    'num_lines': 21,
    'pos_tol': 1e-2,
    'gap_tol': 0.2,
    'move_tol': 0.3,
    'iterator': range(10, 36, 4),
    'min_neighbour_dist': 2e-2
}
##########################################################
############## Defining Settings #########################
##########################################################





##########################################################
############## Defining Surface ##########################
##########################################################
# creating the surface
surface = lambda s, t: [s, s, t]
##########################################################
############## Defining Surface ##########################
##########################################################



##########################################################
############## Run Calculation ###########################
##########################################################
#running z2pack calculations
os.makedirs('results', exist_ok=True)
res_plus = z2pack.surface.run(
    system=snte_plus,
    surface=surface,
    save_file='results/res_plus_m1.json',
    load=True,
    **settings
)

res_minus = z2pack.surface.run(
    system=snte_minus,
    surface=surface,
    save_file='results/res_minus_m1.json',
    load=True,
    **settings
)
##########################################################
############## Run Calculation ###########################
##########################################################


##########################################################
############## Plot and Print ############################
##########################################################
# printing the Chern numbers
print('Chern number for +i eigenstates:', z2pack.invariant.chern(res_plus))
print('Chern number for -i eigenstates:', z2pack.invariant.chern(res_minus))

# creating plots
fig = plt.figure()
ax = fig.add_subplot(1, 2, 1)
ax.set_title("Chern number= {:5.3f}".format(z2pack.invariant.chern(res_plus)))
z2pack.plot.wcc(res_plus, axis=ax, gaps=False)
z2pack.plot.chern(res_plus, axis=ax)

ax = fig.add_subplot(1, 2, 2)
ax.set_title("Chern number= {:5.3f}".format(z2pack.invariant.chern(res_minus)))
z2pack.plot.wcc(res_minus, axis=ax, gaps=False)
z2pack.plot.chern(res_minus, axis=ax)

os.makedirs('plots', exist_ok=True)
plt.savefig('plots/plot_m1.png', bbox_inches='tight')
##########################################################
############## Plot and Print ############################
##########################################################

