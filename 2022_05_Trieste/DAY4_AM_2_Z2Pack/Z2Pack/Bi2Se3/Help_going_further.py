#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess

import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

import z2pack

# Edit the paths to your Quantum Espresso and Wannier90 here
#qedir = '/home/inigo/Documents/Codes/QE-5.3-pw2z2pack_parallel/build-intel-2017b/bin'
qedir = '/home/inigo/Documents/Codes/qe-7.0-ReleasePack/qe-7.0/bin'
wandir = ''

# Commands to run pw, pw2wannier90, wannier90
mpirun = 'mpirun -np 10 '
pwcmd = mpirun + qedir + '/pw.x '
pw2wancmd = mpirun + qedir + '/pw2wannier90.x '
wancmd = wandir + 'wannier90.x'

z2cmd = (
    wancmd + ' -pp bi2se3;' + pwcmd + '-inp bi2se3.nscf.in >& pw.log;' + pw2wancmd +
    '-inp bi2se3.pw2wan.in >& pw2wan.log;'
)

# creating the results folder, running the SCF calculation if needed
if not os.path.exists('./plots'):
    os.mkdir('./plots')
if not os.path.exists('./results'):
    os.mkdir('./results')
if not os.path.exists('./scf'):
    os.makedirs('./scf')
    print("Running the scf calculation")
    shutil.copyfile('input/bi2se3.scf.in', 'scf/bi2se3.scf.in')
    out = subprocess.call(
        pwcmd + ' < bi2se3.scf.in > scf.out', shell=True, cwd='./scf'
    )
    if out != 0:
        raise RuntimeError(
            'Error in SCF call. Inspect scf folder for details, and delete it to re-run the SCF calculation.'
        )


# Creating the System. Note that the SCF charge file does not need to be
# copied, but instead can be referenced in the .files file.
# The k-points input is appended to the .in file
input_files = [
    'input/' + name for name in ["bi2se3.nscf.in", "bi2se3.pw2wan.in", "bi2se3.win"]
]

settings = {
    'num_lines': 21,
    'pos_tol': 1e-1,
    'gap_tol': 0.3,
    'move_tol': 0.4,
    'iterator': range(10, 70, 6),
    'min_neighbour_dist': 2e-2
}

system = z2pack.fp.System(
    input_files=input_files,
    kpt_fct=[z2pack.fp.kpoint.qe_explicit, z2pack.fp.kpoint.wannier90_full],
    kpt_path=["bi2se3.nscf.in", "bi2se3.win"],
    command=z2cmd,
    executable='/bin/bash',
    mmn_path='bi2se3.mmn'
)

# Run the WCC calculations
result_kx_0 = z2pack.surface.run(
    system=system,
    surface=lambda s, t: [0, s / 2, t],
    save_file='./results/res_kx_0.json',
    load=True,
    **settings
)

result_kx_pi = z2pack.surface.run(
    system=system,
    surface=lambda s, t: [0.5, s / 2, t],
    save_file='./results/res_kx_pi.json',
    load=True,
    **settings
)

result_ky_0 = z2pack.surface.run(
    system=system,
    surface=lambda s, t: [t, 0, s / 2],
    save_file='./results/res_ky_0.json',
    load=True,
    **settings
)

result_ky_pi = z2pack.surface.run(
    system=system,
    surface=lambda s, t: [t, 0.5, s / 2],
    save_file='./results/res_ky_pi.json',
    load=True,
    **settings
)

result_kz_0 = z2pack.surface.run(
    system=system,
    surface=lambda s, t: [s / 2, t, 0],
    save_file='./results/res_kz_0.json',
    load=True,
    **settings
)

result_kz_pi = z2pack.surface.run(
    system=system,
    surface=lambda s, t: [s / 2, t, 0.5],
    save_file='./results/res_kz_pi.json',
    load=True,
    **settings
)

# Combining the two plots
fig, ax = plt.subplots(2, 3, sharey=True, figsize=(7, 9))

ax[0,0].set_title('$k_x=0$ $Z_2$ = {0}'.format(z2pack.invariant.z2(result_kx_0)))
ax[0,1].set_title('$k_y=0$ $Z_2$ = {0}'.format(z2pack.invariant.z2(result_ky_0)))
ax[0,2].set_title('$k_z=0$ $Z_2$ = {0}'.format(z2pack.invariant.z2(result_kz_0)))
ax[1,0].set_title('$k_x=\pi$ $Z_2$ = {0}'.format(z2pack.invariant.z2(result_kx_pi)))
ax[1,1].set_title('$k_y=\pi$ $Z_2$ = {0}'.format(z2pack.invariant.z2(result_ky_pi)))
ax[1,2].set_title('$k_z=\pi$ $Z_2$ = {0}'.format(z2pack.invariant.z2(result_kz_pi)))

z2pack.plot.wcc(result_kx_0, axis=ax[0,0], gaps=False)
z2pack.plot.wcc(result_ky_0, axis=ax[0,1], gaps=False)
z2pack.plot.wcc(result_kz_0, axis=ax[0,2], gaps=False)
z2pack.plot.wcc(result_kx_pi, axis=ax[1,0], gaps=False)
z2pack.plot.wcc(result_ky_pi, axis=ax[1,1], gaps=False)
z2pack.plot.wcc(result_kz_pi, axis=ax[1,2], gaps=False)
plt.savefig('plots/plot.png', bbox_inches='tight')
