#!/usr/bin/env python

# Haldane model from Phys. Rev. Lett. 61, 2015 (1988)
# Calculates Berry phases and curvatures for this model

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

# make two dimensional tight-binding Haldane model
my_model=tb_model(2,2,lat,orb)

# set model parameters
delta=0.0
t=-1.0
t2 =0.15*np.exp((1.j)*np.pi/2.)
t2c=t2.conjugate()

# set on-site energies
my_model.set_onsite([-delta,delta])
# set hoppings (one for each connected pair of orbitals)
# (amplitude, i, j, [lattice vector to cell containing j])
my_model.set_hop(t, 0, 1, [ 0, 0])
my_model.set_hop(t, 1, 0, [ 1, 0])
my_model.set_hop(t, 1, 0, [ 0, 1])
# add second neighbour complex hoppings
my_model.set_hop(t2 , 0, 0, [ 1, 0])
my_model.set_hop(t2 , 1, 1, [ 1,-1])
my_model.set_hop(t2 , 1, 1, [ 0, 1])
my_model.set_hop(t2c, 1, 1, [ 1, 0])
my_model.set_hop(t2c, 0, 0, [ 1,-1])
my_model.set_hop(t2c, 0, 0, [ 0, 1])

# print tight-binding model details
my_model.display()

print(r"Using approach #1")
# approach #1
# generate object of type wf_array that will be used for
# Berry phase and curvature calculations
my_array_1=wf_array(my_model,[31,31])
# solve model on a regular grid, and put origin of
# Brillouin zone at -1/2 -1/2 point
my_array_1.solve_on_grid([-0.5,-0.5])

# calculate Berry phases around the BZ in the k_x direction
# (which can be interpreted as the 1D hybrid Wannier center
# in the x direction) and plot results as a function of k_y
#
# Berry phases along k_x for lower band
phi_a_1 = my_array_1.berry_phase([0],0,contin=True)
# Berry phases along k_x for upper band
phi_b_1 = my_array_1.berry_phase([1],0,contin=True)
# Berry phases along k_x for both bands
phi_c_1 = my_array_1.berry_phase([0,1],0,contin=True)

# Berry flux for lower band
flux_a_1=my_array_1.berry_flux([0])

# plot Berry phases
fig, ax = plt.subplots()
ky=np.linspace(0.,1.,len(phi_a_1))
ax.plot(ky,phi_a_1, 'ro')
ax.plot(ky,phi_b_1, 'go')
ax.plot(ky,phi_c_1, 'bo')
ax.set_title("Berry phase for lower (red), top (green), both bands (blue)")
ax.set_xlabel(r"$k_y$")
ax.set_ylabel(r"Berry phase along $k_x$")
ax.set_xlim(0.,1.)
ax.set_ylim(-7.,7.)
ax.yaxis.set_ticks([-2.*np.pi,-np.pi,0.,np.pi,2.*np.pi])
ax.set_yticklabels((r'$-2\pi$',r'$-\pi$',r'$0$',r'$\pi$', r'$2\pi$'))
fig.tight_layout()
fig.savefig("haldane_bp_phase.pdf")
# print out info about flux
print(" Berry flux= ",flux_a_1)

print(r"Using approach #2")
# approach #2
# do the same thing as in approach #1 but do not use
# automated solver
#
# intialize k-space mesh
nkx=31
nky=31
kx=np.linspace(-0.5,0.5,num=nkx)
ky=np.linspace(-0.5,0.5,num=nky)
# initialize object to store all wavefunctions
my_array_2=wf_array(my_model,[nkx,nky])
# solve model at all k-points
for i in range(nkx):
    for j in range(nky):
        (eval,evec)=my_model.solve_one([kx[i],ky[j]],eig_vectors=True)
        # store wavefunctions
        my_array_2[i,j]=evec
# impose periodic boundary conditions in both k_x and k_y directions
my_array_2.impose_pbc(0,0)
my_array_2.impose_pbc(1,1)
# calculate Berry flux for lower band
flux_a_2=my_array_2.berry_flux([0])

# print out info about curvature
print(" Berry flux= ",flux_a_2)

print('Done.\n')
