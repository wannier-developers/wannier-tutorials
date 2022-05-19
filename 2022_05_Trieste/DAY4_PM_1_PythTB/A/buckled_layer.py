#!/usr/bin/env python

# buckled layer model on rectangular lattice
# illustrates usage of function k_path

# Copyright under GNU General Public License 2010, 2012, 2016
# by Sinisa Coh and David Vanderbilt (see gpl-pythtb.txt)

from __future__ import print_function
from pythtb import * # import TB model class
import numpy as np
import matplotlib.pyplot as plt

# real space is 3D
# define lattice vectors
lat=[[1.0,0.0,0.0],[0.0,1.25,0.0],[0.0,0.0,3.0]]
# define coordinates of orbitals
orb=[[0.0,0.0,-0.15],[0.5,0.5,0.15]]

# only first two lattice vectors repeat, so k-space is 2D
my_model=tb_model(2,3,lat,orb)

# set model parameters
delta=1.1
t=0.6

# set on-site energies
my_model.set_onsite([-delta,delta])
# set hoppings (one for each connected pair of orbitals)
# (amplitude, i, j, [lattice vector to cell containing j])
my_model.set_hop(t, 1, 0, [0, 0, 0])
my_model.set_hop(t, 1, 0, [1, 0, 0])
my_model.set_hop(t, 1, 0, [0, 1, 0])
my_model.set_hop(t, 1, 0, [1, 1, 0])

# print tight-binding model
my_model.display()

# ----------------------------------------
# specify k-space path
# ----------------------------------------

# specify a path in k-space by listing a set of nodes; the path
# will consist of straight line segments connecting these nodes
path=[[0.0,0.0],[0.0,0.5],[0.5,0.5],[0.0,0.0]]

# specify labels for these nodal points
label=(r'$\Gamma $',r'$X$', r'$M$', r'$\Gamma $')

# call function k_path to construct the actual path
(k_vec,k_dist,k_node)=my_model.k_path(path,81)
# inputs:
#   path: see above
#   81: number of interpolated k-points to be plotted
# outputs:
#   k_vec: list of interpolated k-points
#   k_dist: horizontal axis position of each k-point in the list
#   k_node: horizontal axis position of each original node

# ----------------------------------------
# do bandstructure calculation
# ----------------------------------------
print('Calculating bandstructure...')
evals=my_model.solve_all(k_vec)

# ----------------------------------------
# plot band structure
# ----------------------------------------
print('Plotting bandstructure...')

# Initialize plot
fig, ax = plt.subplots()
ax.set_title("Bandstructure for buckled rectangular layer")
ax.set_ylabel("Band energy")

# specify horizontal axis details
ax.set_xlim(k_node[0],k_node[-1])
# put tickmarks and labels at node positions
ax.set_xticks(k_node)
ax.set_xticklabels(label)
# add vertical lines at node positions
for n in range(len(k_node)):
  ax.axvline(x=k_node[n],linewidth=0.5, color='k')

# Plot two bands
ax.plot(k_dist,evals[0])
ax.plot(k_dist,evals[1])

# save as PDF
fig.tight_layout()
fig.savefig("buckled_layer.pdf")

print('Done.\n')
