#!/usr/bin/env python

# zero dimensional tight-binding model of a NH3 molecule

# Copyright under GNU General Public License 2010, 2012, 2016
# by Sinisa Coh and David Vanderbilt (see gpl-pythtb.txt)

from __future__ import print_function
from pythtb import * # import TB model class
import numpy as np
import matplotlib.pyplot as plt

# define lattice vectors
lat=[[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]]
# define coordinates of orbitals
sq32=np.sqrt(3.0)/2.0
orb=[[ (2./3.)*sq32, 0.   ,0.],
     [(-1./3.)*sq32, 1./2.,0.],
     [(-1./3.)*sq32,-1./2.,0.],
     [  0.         , 0.   ,1.]]
# make zero dimensional tight-binding model
my_model=tb_model(0,3,lat,orb)

# set model parameters
delta=0.5
t_first=1.0

# change on-site energies so that N and H don't have the same energy
my_model.set_onsite([-delta,-delta,-delta,delta])
# set hoppings (one for each connected pair of orbitals)
# (amplitude, i, j)
my_model.set_hop(t_first, 0, 1)
my_model.set_hop(t_first, 0, 2)
my_model.set_hop(t_first, 0, 3)
my_model.set_hop(t_first, 1, 2)
my_model.set_hop(t_first, 1, 3)
my_model.set_hop(t_first, 2, 3)

# print tight-binding model
my_model.display()

print('---------------------------------------')
print('starting calculation')
print('---------------------------------------')
print('Calculating bands...')
print()
print('Band energies')
print()    
# solve for eigenenergies of hamiltonian
evals=my_model.solve_all()

# First make a figure object
fig, ax = plt.subplots()
# plot all states
ax.plot(evals,"bo")
ax.set_xlim(-0.3,3.3)
ax.set_ylim(evals.min()-0.5,evals.max()+0.5)
# put title
ax.set_title("Molecule levels")
ax.set_xlabel("Orbital")
ax.set_ylabel("Energy")
# make an PDF figure of a plot
fig.tight_layout()
fig.savefig("0dim_spectrum.pdf")                    

print('Done.\n')
