#!/usr/bin/env python

# one-dimensional family of tight binding models
# parametrized by one parameter, lambda

# Copyright under GNU General Public License 2010, 2012, 2016
# by Sinisa Coh and David Vanderbilt (see gpl-pythtb.txt)

from __future__ import print_function
from pythtb import * # import TB model class
import numpy as np
import matplotlib.pyplot as plt

# define function to construct model
def set_model(t,delta,lmbd):
    lat=[[1.0]]
    orb=[[0.0],[1.0/3.0],[2.0/3.0]]
    model=tb_model(1,1,lat,orb)
    model.set_hop(t, 0, 1, [0])
    model.set_hop(t, 1, 2, [0])
    model.set_hop(t, 2, 0, [1])
    onsite_0=delta*(-1.0)*np.cos(2.0*np.pi*(lmbd-0.0/3.0))
    onsite_1=delta*(-1.0)*np.cos(2.0*np.pi*(lmbd-1.0/3.0))
    onsite_2=delta*(-1.0)*np.cos(2.0*np.pi*(lmbd-2.0/3.0))
    model.set_onsite([onsite_0,onsite_1,onsite_2])
    return(model)

# set model parameters
delta=2.0
t=-1.3

# evolve tight-binding parameter lambda along a path
path_steps=21
all_lambda=np.linspace(0.0,1.0,path_steps,endpoint=True)

# get model at arbitrary lambda for initializations
my_model=set_model(t,delta,0.)

# set up 1d Brillouin zone mesh
num_kpt=31
(k_vec,k_dist,k_node)=my_model.k_path([[-0.5],[0.5]],num_kpt,report=False)

# two-dimensional wf_array in which we will store wavefunctions
# we store it in the order [lambda,k] since want Berry curvatures
#   and Chern numbers defined with the [lambda,k] sign convention
wf_kpt_lambda=wf_array(my_model,[path_steps,num_kpt])

# fill the array with eigensolutions
for i_lambda in range(path_steps):
    lmbd=all_lambda[i_lambda]
    my_model=set_model(t,delta,lmbd)
    (eval,evec)=my_model.solve_all(k_vec,eig_vectors=True)
    for i_kpt in range(num_kpt):
        wf_kpt_lambda[i_lambda,i_kpt]=evec[:,i_kpt,:]

# compute integrated curvature
print("Chern numbers for rising fillings")
print("  Band  0     = %5.2f" % (wf_kpt_lambda.berry_flux([0])/(2.*np.pi)))
print("  Bands 0,1   = %5.2f" % (wf_kpt_lambda.berry_flux([0,1])/(2.*np.pi)))
print("  Bands 0,1,2 = %5.2f" % (wf_kpt_lambda.berry_flux([0,1,2])/(2.*np.pi)))
print("")
print("Chern numbers for individual bands")
print("  Band  0 = %5.2f" % (wf_kpt_lambda.berry_flux([0])/(2.*np.pi)))
print("  Band  1 = %5.2f" % (wf_kpt_lambda.berry_flux([1])/(2.*np.pi)))
print("  Band  2 = %5.2f" % (wf_kpt_lambda.berry_flux([2])/(2.*np.pi)))
print("")

# for annotating plot with text
text_lower="C of band [0] = %3.0f" % (wf_kpt_lambda.berry_flux([0])/(2.*np.pi))
text_upper="C of bands [0,1] = %3.0f" % (wf_kpt_lambda.berry_flux([0,1])/(2.*np.pi))

# now loop over parameter again, this time for finite chains
path_steps=241
all_lambda=np.linspace(0.0,1.0,path_steps,endpoint=True)

# length of chain, in unit cells
num_cells=10
num_orb=3*num_cells

# initialize array for chain eigenvalues and x expectations
ch_eval=np.zeros([num_orb,path_steps],dtype=float)
ch_xexp=np.zeros([num_orb,path_steps],dtype=float)

for i_lambda in range(path_steps):
    lmbd=all_lambda[i_lambda]

    # construct and solve model
    my_model=set_model(t,delta,lmbd)
    ch_model=my_model.cut_piece(num_cells,0)
    (eval,evec)=ch_model.solve_all(eig_vectors=True)

    # save eigenvalues
    ch_eval[:,i_lambda]=eval
    ch_xexp[:,i_lambda]=ch_model.position_expectation(evec,0)

# plot eigenvalues vs. lambda
# symbol size is reduced for states localized near left end

(fig, ax) = plt.subplots()

# loop over "bands"
for n in range(num_orb):
    # diminish the size of the ones on the borderline
    xcut=2.   # discard points below this
    xfull=4.  # use sybols of full size above this
    size=(ch_xexp[n,:]-xcut)/(xfull-xcut)
    for i in range(path_steps):
        size[i]=min(size[i],1.)
        size[i]=max(size[i],0.1)
    ax.scatter(all_lambda[:],ch_eval[n,:], edgecolors='none', s=size*6., c='k')

# annotate gaps with bulk Chern numbers calculated earlier
ax.text(0.20,-1.7,text_lower)
ax.text(0.45, 1.5,text_upper)

ax.set_title("Eigenenergies for finite chain of 3-site-model")
ax.set_xlabel(r"Parameter $\lambda$") 
ax.set_ylabel("Energy")
ax.set_xlim(0.,1.)
fig.tight_layout()
fig.savefig("3site_endstates.pdf")

print('Done.\n')
