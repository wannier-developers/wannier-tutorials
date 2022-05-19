#!/usr/bin/env python

# Make arbitrary surface of the graphene model using
# make_supercell method.

# Copyright under GNU General Public License 2010, 2012, 2016
# by Sinisa Coh and David Vanderbilt (see gpl-pythtb.txt)

from __future__ import print_function
from pythtb import * # import TB model class
import numpy as np
import matplotlib.pyplot as plt

# define lattice vectors
lat=[[1.0,0.0],[0.5,np.sqrt(3.0)/2.0]]
# define coordinates of orbitals
orb=[[1./3.,1./3.],[2./3.,2./3.]]

# make two dimensional tight-binding graphene model
my_model=tb_model(2,2,lat,orb)

# set model parameters
delta=0.0
t=-1.0

# set on-site energies
my_model.set_onsite([-delta,delta])
# set hoppings (one for each connected pair of orbitals)
# (amplitude, i, j, [lattice vector to cell containing j])
my_model.set_hop(t, 0, 1, [ 0, 0])
my_model.set_hop(t, 1, 0, [ 1, 0])
my_model.set_hop(t, 1, 0, [ 0, 1])

# make the supercell of the model
sc_model=my_model.make_supercell([[2,1],[-1,2]],to_home=True)

# now make a slab of the supercell
slab_model=sc_model.cut_piece(6,1,glue_edgs=False)

# visualize slab unit cell
(fig,ax)=slab_model.visualize(0,1)
ax.set_title("Graphene, arbitrary surface")
ax.set_xlabel("x coordinate")
ax.set_ylabel("y coordinate")
fig.tight_layout()
fig.savefig("supercell_vis.pdf")

# compute the band structure in the entire band
(k_vec,k_dist,k_node)=slab_model.k_path('full',100)
evals=slab_model.solve_all(k_vec)

# plotting of band structure
print('Plotting bandstructure...')

# First make a figure object
fig, ax = plt.subplots()
# plot all bands
for i in range(evals.shape[0]):
    ax.plot(k_dist,evals[i],"k-")
# zoom in close to the zero energy
ax.set_xlim(k_dist[0],k_dist[-1])
ax.set_ylim(-1.0,1.0)
# put title on top
ax.set_title("Graphene arbitrary surface band structure")
ax.set_xlabel("k parallel to edge")
ax.set_ylabel("Band energy")
ax.xaxis.set_ticks(k_node)
ax.set_xticklabels((r'$0$',r'$\pi$',r'$2\pi$'))
# make an PDF figure of a plot
fig.tight_layout()
fig.savefig("supercell_band.pdf")

print('Done.\n')
