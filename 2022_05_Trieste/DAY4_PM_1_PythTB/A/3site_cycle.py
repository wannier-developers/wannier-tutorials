#!/usr/bin/env python

# one-dimensional family of tight binding models
# parametrized by one parameter, lambda

# Copyright under GNU General Public License 2010, 2012, 2016
# by Sinisa Coh and David Vanderbilt (see gpl-pythtb.txt)

from __future__ import print_function
from pythtb import * # import TB model class
import numpy as np
import matplotlib.pyplot as plt

# define lattice vectors
lat=[[1.0]]
# define coordinates of orbitals
orb=[[0.0],[1.0/3.0],[2.0/3.0]]

# make one dimensional tight-binding model
my_model=tb_model(1,1,lat,orb)

# set model parameters
delta=2.0
t=-1.0

# set hoppings (one for each connected pair of orbitals)
# (amplitude, i, j, [lattice vector to cell containing j])
my_model.set_hop(t, 0, 1, [0])
my_model.set_hop(t, 1, 2, [0])
my_model.set_hop(t, 2, 0, [1])

# plot onsite terms for each site
fig_onsite, ax_onsite = plt.subplots()
# plot band structure for each lambda
fig_band,   ax_band   = plt.subplots()

# evolve tight-binding parameter along some path by
# performing a change of onsite terms
#   how many steps to take along the path (including end points)
path_steps=21
#   create lambda mesh from 0.0 to 1.0 (21 values and 20 intervals)
all_lambda=np.linspace(0.0,1.0,path_steps,endpoint=True)
#   how many k-points to use (31 values and 30 intervals)
num_kpt=31
# two-dimensional wf_array in which we will store wavefunctions
# for all k-points and all values of lambda.  (note that the index
# order [k,lambda] is important for interpreting the sign.)
wf_kpt_lambda=wf_array(my_model,[num_kpt,path_steps])
for i_lambda in range(path_steps):
    # for each step along the path compute onsite terms for each orbital
    lmbd=all_lambda[i_lambda]
    onsite_0=delta*(-1.0)*np.cos(2.0*np.pi*(lmbd-0.0/3.0))
    onsite_1=delta*(-1.0)*np.cos(2.0*np.pi*(lmbd-1.0/3.0))
    onsite_2=delta*(-1.0)*np.cos(2.0*np.pi*(lmbd-2.0/3.0))

    # update onsite terms by rewriting previous values
    my_model.set_onsite([onsite_0,onsite_1,onsite_2],mode="reset")

    # create k mesh over 1D Brillouin zone
    (k_vec,k_dist,k_node)=my_model.k_path([[-0.5],[0.5]],num_kpt,report=False)
    # solve model on all of these k-points
    (eval,evec)=my_model.solve_all(k_vec,eig_vectors=True)
    # store wavefunctions (eigenvectors)
    for i_kpt in range(num_kpt):
        wf_kpt_lambda[i_kpt,i_lambda]=evec[:,i_kpt,:]

    # plot on-site terms
    ax_onsite.scatter([lmbd],[onsite_0],c="r")
    ax_onsite.scatter([lmbd],[onsite_1],c="g")
    ax_onsite.scatter([lmbd],[onsite_2],c="b")
    # plot band structure for all three bands
    for band in range(eval.shape[0]):
        ax_band.plot(k_dist,eval[band,:],"k-",linewidth=0.5)

# impose periodic boundary condition along k-space direction only
# (so that |psi_nk> at k=0 and k=1 have the same phase)
wf_kpt_lambda.impose_pbc(0,0)

# compute Berry phase along k-direction for each lambda
phase=wf_kpt_lambda.berry_phase([0],0)

# plot position of Wannier function for bottom band
fig_wann, ax_wann = plt.subplots()
# wannier center in reduced coordinates
wann_center=phase/(2.0*np.pi)
# plot wannier centers
ax_wann.plot(all_lambda,wann_center,"ko-")

# compute integrated curvature
final=wf_kpt_lambda.berry_flux([0])
print("Berry flux in k-lambda space: ",final)

# finish plot of onsite terms
ax_onsite.set_title("Onsite energy for all three orbitals")
ax_onsite.set_xlabel("Lambda parameter")
ax_onsite.set_ylabel("Onsite terms")
ax_onsite.set_xlim(0.0,1.0)
fig_onsite.tight_layout()
fig_onsite.savefig("3site_onsite.pdf")
# finish plot for band structure
ax_band.set_title("Band structure")
ax_band.set_xlabel("Path in k-vector")
ax_band.set_ylabel("Band energies")
ax_band.set_xlim(0.0,1.0)
fig_band.tight_layout()
fig_band.savefig("3site_band.pdf")
# finish plot for Wannier center
ax_wann.set_title("Center of Wannier function")
ax_wann.set_xlabel("Lambda parameter")
ax_wann.set_ylabel("Center (reduced coordinate)")
ax_wann.set_xlim(0.0,1.0)
fig_wann.tight_layout()
fig_wann.savefig("3site_wann.pdf")

print('Done.\n')
