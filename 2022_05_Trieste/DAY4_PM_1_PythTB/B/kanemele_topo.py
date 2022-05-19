#!/usr/bin/env python
from __future__ import print_function # python3 style print

# Tight-binding 2D Kane-Mele model
# C.L. Kane and E.J. Mele, PRL 95, 146802 (2005)

from pythtb import * # import TB model class
import matplotlib.pyplot as plt

# set model parameters
delta=0.7     # site energy
t=-1.0        # spin-independent first-neighbor hop
soc=0.06      # spin-dependent second-neighbor hop
rashba=0.05   # spin-flip first-neighbor hop
soc_list=[-0.06,-0.24] # spin-dependent second-neighbor hop

def set_model(t,soc,rashba,delta):

  # set up Kane-Mele model
  lat=[[1.0,0.0],[0.5,np.sqrt(3.0)/2.0]]
  orb=[[1./3.,1./3.],[2./3.,2./3.]]
  model=tb_model(2,2,lat,orb,nspin=2)
  model.set_onsite([delta,-delta])

  # definitions of Pauli matrices
  sigma_x=np.array([0.,1.,0.,0])
  sigma_y=np.array([0.,0.,1.,0])
  sigma_z=np.array([0.,0.,0.,1])
  r3h =np.sqrt(3.0)/2.0
  sigma_a= 0.5*sigma_x-r3h*sigma_y
  sigma_b= 0.5*sigma_x+r3h*sigma_y
  sigma_c=-1.0*sigma_x

  # spin-independent first-neighbor hops
  for lvec in ([ 0, 0], [-1, 0], [ 0,-1]):
    model.set_hop(t, 0, 1, lvec)
  # spin-dependent second-neighbor hops
  for lvec in ([ 1, 0], [-1, 1], [ 0,-1]):
    model.set_hop(soc*1.j*sigma_z, 0, 0, lvec)
  for lvec in ([-1, 0], [ 1,-1], [ 0, 1]):
    model.set_hop(soc*1.j*sigma_z, 1, 1, lvec)
  # spin-flip first-neighbor hops
  model.set_hop(1.j*rashba*sigma_a, 0, 1, [ 0, 0], mode="add")
  model.set_hop(1.j*rashba*sigma_b, 0, 1, [-1, 0], mode="add")
  model.set_hop(1.j*rashba*sigma_c, 0, 1, [ 0,-1], mode="add")

  return model

# For the purposes of plot labels:
#   Real space is (r1,r2) in reduced coordinates
#   Reciprocal space is (k1,k2) in reduced coordinates
# Below, following Python, these are (r0,r1) and (k0,k1)

# set up figures
fig,ax=plt.subplots(2,2,figsize=(7,6))

nk=51
# run over two choices of t2
for je,soc in enumerate(soc_list):

  # solve bulk model on grid and get hybrid Wannier centers along r1
  # as a function of k0
  my_model=set_model(t,soc,rashba,delta)
  my_array=wf_array(my_model,[nk,nk])
  my_array.solve_on_grid([0.,0.])
  rbar = my_array.berry_phase([0,1],1,berry_evals=True,contin=True)/(2.*np.pi)
  
  # set up and solve ribbon model that is finite along direction 1
  width=20
  nkr=81
  ribbon_model=my_model.cut_piece(width,fin_dir=1,glue_edgs=False)
  (k_vec,k_dist,k_node)=ribbon_model.k_path('full',nkr,report=False)
  (rib_eval,rib_evec)=ribbon_model.solve_all(k_vec,eig_vectors=True)
  
  nbands=rib_eval.shape[0]
  (ax0,ax1)=ax[je,:]
  
  # hybrid Wannier center flow
  k0=np.linspace(0.,1.,nk)
  ax0.set_xlim(0.,1.)
  ax0.set_ylim(-1.3,1.3)
  ax0.set_xlabel(r"$\kappa_1/2\pi$")
  ax0.set_ylabel(r"HWF centers")
  ax0.axvline(x=0.5,linewidth=0.5, color='k')
  for shift in (-1.,0.,1.,2.):
    ax0.plot(k0,rbar[:,0]+shift,color='k')
    ax0.plot(k0,rbar[:,1]+shift,color='k')
  
  # edge band structure
  k0=np.linspace(0.,1.,nkr)
  ax1.set_xlim(0.,1.)
  ax1.set_ylim(-2.5,2.5)
  ax1.set_xlabel(r"$\kappa_1/2\pi$")
  ax1.set_ylabel(r"Edge band structure")
  for (i,kv) in enumerate(k0):
  
    # find expectation value <r1> at i'th k-point along direction k0
    pos_exp=ribbon_model.position_expectation(rib_evec[:,i],dir=1)
  
    # assign weight in [0,1] to be 1 except for edge states near bottom
    weight=3.0*pos_exp/width
    for j in range(nbands):
      weight[j]=min(weight[j],1.)
  
    # scatterplot with symbol size proportional to assigned weight
    s=ax1.scatter([k_vec[i]]*nbands, rib_eval[:,i],
         s=0.6+2.5*weight, c='k', marker='o', edgecolors='none')

    #   ax0.text(-0.45,0.92,'(a)',size=18.,transform=ax0.transAxes)
    #   ax1.text(-0.45,0.92,'(b)',size=18.,transform=ax1.transAxes)

# save figure as a PDF
aa=ax.flatten()
for i,lab in enumerate(['(a)','(b)','(c)','(d)']):
  aa[i].text(-0.45,0.92,lab,size=18.,transform=aa[i].transAxes)
fig.tight_layout()
plt.subplots_adjust(left=0.15,wspace=0.6)
fig.savefig("kanemele_topo.pdf")
