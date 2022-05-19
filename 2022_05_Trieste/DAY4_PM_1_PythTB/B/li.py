#!/usr/bin/env python
from __future__ import print_function # python3 style print

# 3D model of Li on bcc lattice, with s orbitals only

from pythtb import * # import TB model class
import matplotlib.pyplot as plt

# define lattice vectors
lat=[[-0.5, 0.5, 0.5],[ 0.5,-0.5, 0.5],[ 0.5, 0.5,-0.5]]
# define coordinates of orbitals
orb=[[0.0,0.0,0.0]]

# make 3D model
my_model=tb_model(3,3,lat,orb)

# set model parameters
# lattice parameter implicitly set to a=1
Es= 4.5    # site energy
t =-1.4    # hopping parameter

# set on-site energy
my_model.set_onsite([Es])
# set hoppings along four unique bonds
# note that neighboring cell must be specified in lattice coordinates
# (the corresponding Cartesian coords are given for reference)
my_model.set_hop(t, 0, 0, [1,0,0])    # [-0.5, 0.5, 0.5] cartesian
my_model.set_hop(t, 0, 0, [0,1,0])    # [ 0.5,-0.5, 0.5] cartesian
my_model.set_hop(t, 0, 0, [0,0,1])    # [ 0.5, 0.5,-0.5] cartesian
my_model.set_hop(t, 0, 0, [1,1,1])    # [ 0.5, 0.5, 0.5] cartesian

# print tight-binding model
my_model.display()

# generate k-point path and labels
# again, specified in reciprocal lattice coordinates
k_P     = [0.25,0.25,0.25]            # [ 0.5, 0.5, 0.5] cartesian
k_Gamma = [ 0.0, 0.0, 0.0]            # [ 0.0, 0.0, 0.0] cartesian
k_H     = [-0.5, 0.5, 0.5]            # [ 1.0, 0.0, 0.0] cartesian
path=[k_P,k_Gamma,k_H]
label=(r'$P$',r'$\Gamma $',r'$H$')
(k_vec,k_dist,k_node)=my_model.k_path(path,101)

print('---------------------------------------')
print('starting calculation')
print('---------------------------------------')
print('Calculating bands...')

# solve for eigenenergies of hamiltonian on
# the set of k-points from above
evals=my_model.solve_all(k_vec)

# plotting of band structure
print('Plotting band structure...')

# First make a figure object
fig, ax = plt.subplots(figsize=(4.,3.))

# specify horizontal axis details
ax.set_xlim([0,k_node[-1]])
ax.set_xticks(k_node)
ax.set_xticklabels(label)
for n in range(len(k_node)):
  ax.axvline(x=k_node[n], linewidth=0.5, color='k')

# plot bands
ax.plot(k_dist,evals[0],color='k')
# put title
ax.set_xlabel("Path in k-space")
ax.set_ylabel("Band energy")
# make a PDF figure of a plot
fig.tight_layout()
fig.savefig("li_bsr.pdf")

print('Done.\n')
