#!/usr/bin/env python

# Haldane model from Phys. Rev. Lett. 61, 2015 (1988)
# First, compute bulk Wannier centers along direction 1
# Then, cut a ribbon that extends along direcion 0, and compute
#   both the edge states and the finite hybrid Wannier centers
#   along direction 1.

# Copyright under GNU General Public License 2010, 2012, 2016
# by Sinisa Coh and David Vanderbilt (see gpl-pythtb.txt)

from __future__ import print_function
from pythtb import * # import TB model class
import numpy as np
import matplotlib.pyplot as plt

# set model parameters
delta=-0.2
t=-1.0
t2 =0.05-0.15j
t2c=t2.conjugate()

# Fermi level, relevant for edge states of ribbon
efermi=0.25  

# define lattice vectors and orbitals and make model
lat=[[1.0,0.0],[0.5,np.sqrt(3.0)/2.0]]
orb=[[1./3.,1./3.],[2./3.,2./3.]]
my_model=tb_model(2,2,lat,orb)

# set on-site energies and hoppings
my_model.set_onsite([-delta,delta])
my_model.set_hop(t, 0, 1, [ 0, 0])
my_model.set_hop(t, 1, 0, [ 1, 0])
my_model.set_hop(t, 1, 0, [ 0, 1])
my_model.set_hop(t2 , 0, 0, [ 1, 0])
my_model.set_hop(t2 , 1, 1, [ 1,-1])
my_model.set_hop(t2 , 1, 1, [ 0, 1])
my_model.set_hop(t2c, 1, 1, [ 1, 0])
my_model.set_hop(t2c, 0, 0, [ 1,-1])
my_model.set_hop(t2c, 0, 0, [ 0, 1])

# number of discretized sites or k-points in the mesh in directions 0 and 1
len_0=100
len_1=10

# compute Berry phases in direction 1 for the bottom band
my_array=wf_array(my_model,[len_0,len_1])
my_array.solve_on_grid([0.0,0.0])
phi_1=my_array.berry_phase(occ=[0], dir=1, contin=True)

# create Haldane ribbon that is finite along direction 1
ribbon_model=my_model.cut_piece(len_1, fin_dir=1, glue_edgs=False)
(k_vec,k_dist,k_node)=ribbon_model.k_path([0.0, 0.5, 1.0],len_0,report=False)
k_label=[r"$0$",r"$\pi$", r"$2\pi$"]

# solve ribbon model to get eigenvalues and eigenvectors
(rib_eval,rib_evec)=ribbon_model.solve_all(k_vec,eig_vectors=True)
# shift bands so that the fermi level is at zero energy
rib_eval-=efermi

# find k-points at which number of states below the Fermi level changes
jump_k=[]
for i in range(rib_eval.shape[1]-1):
  nocc_i =np.sum(rib_eval[:,i]<0.0)
  nocc_ip=np.sum(rib_eval[:,i+1]<0.0)
  if nocc_i!=nocc_ip:
    jump_k.append(i)

# plot expectation value of position operator for states in the ribbon
# and hybrid Wannier function centers
fig, (ax1, ax2) = plt.subplots(2,1,figsize=(3.7,4.5))

# plot bandstructure of the ribbon
for n in range(rib_eval.shape[0]):
  ax1.plot(k_dist,rib_eval[n,:],c='k', zorder=-50)

# color bands according to expectation value of y operator (red=top, blue=bottom)
for i in range(rib_evec.shape[1]):
  # get expectation value of the position operator for states at i-th kpoint
  pos_exp=ribbon_model.position_expectation(rib_evec[:,i],dir=1)

  # plot states according to the expectation value
  s=ax1.scatter([k_vec[i]]*rib_eval.shape[0], rib_eval[:,i], c=pos_exp, s=7,
                marker='o', cmap="coolwarm", edgecolors='none', vmin=0.0, vmax=float(len_1), zorder=-100)

# color scale
fig.colorbar(s,None,ax1,ticks=[0.0,float(len_1)])

# plot Fermi energy
ax1.axhline(0.0,c='m',zorder=-200)

# vertical lines show crossings of surface bands with Fermi energy
for ax in [ax1,ax2]:
  for i in jump_k:
    ax.axvline(x=(k_vec[i]+k_vec[i+1])/2.0, linewidth=0.7, color='k',zorder=-150)

# tweaks
ax1.set_ylabel("Ribbon band energy")
ax1.set_ylim(-2.3,2.3)

# bottom plot shows Wannier center flow
#   bulk Wannier centers in green lines
#   finite-ribbon Wannier centers in black dots
# compare with Fig 3 in Phys. Rev. Lett. 102, 107603 (2009)

# plot bulk hybrid Wannier center positions and their periodic images
for j in range(-1,len_1+1):
    ax2.plot(k_vec,float(j)+phi_1/(2.0*np.pi),'k-',zorder=-50)

# plot finite centers of ribbon along direction 1
for i in range(rib_evec.shape[1]):
  # get occupied states only (those below Fermi level)
  occ_evec=rib_evec[rib_eval[:,i]<0.0,i]
  # get centers of hybrid wannier functions
  hwfc=ribbon_model.position_hwf(occ_evec,1)
  # plot centers
  s=ax2.scatter([k_vec[i]]*hwfc.shape[0], hwfc, c=hwfc, s=7,
                marker='o', cmap="coolwarm", edgecolors='none', vmin=0.0, vmax=float(len_1), zorder=-100)

# color scale
fig.colorbar(s,None,ax2,ticks=[0.0,float(len_1)])

# tweaks
ax2.set_xlabel(r"k vector along direction 0")
ax2.set_ylabel(r"Wannier center along direction 1")
ax2.set_ylim(-0.5,len_1+0.5)
  
# label both axes
for ax in [ax1,ax2]:
  ax.set_xlim(k_node[0],k_node[-1])
  ax.set_xticks(k_node)
  ax.set_xticklabels(k_label)

fig.tight_layout()
fig.savefig("haldane_hwf.pdf")

print('Done.\n')



