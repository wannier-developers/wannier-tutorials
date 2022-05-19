#!/usr/bin/env python
from __future__ import print_function # python3 style print

# Chain with alternating site energies and hoppings

from pythtb import *
import matplotlib.pyplot as plt

# define function to set up model for a given parameter set
def set_model(t,del_t,Delta):
  lat=[[1.0]]
  orb=[[0.0],[0.5]]
  my_model=tbmodel(1,1,lat,orb)
  my_model.set_onsite([Delta,-Delta])
  my_model.add_hop(t+del_t, 0, 1, [0])
  my_model.add_hop(t-del_t, 1, 0, [1])
  return my_model

# set parameters of model
t=-1.0       # average hopping
del_t=-0.3   # bond strength alternation
Delta= 0.4   # site energy alternation
my_model=set_model(t,del_t,Delta)
my_model.display()

# -----------------------------------
# explicit calculation of Berry phase
# -----------------------------------

# set up and solve the model on a discretized k mesh
nk=61          # 60 equal intervals around the unit circle
(k_vec,k_dist,k_node)=my_model.k_path('full',nk,report=False)
(eval,evec)=my_model.solve_all(k_vec,eig_vectors=True)
evec=evec[0]   # pick band=0 from evec[band,kpoint,orbital]
               # now just evec[kpoint,orbital]

# k-points 0 and 60 refer to the same point on the unit circle
# so we will work only with evec[0],...,evec[59]

# compute Berry phase of lowest band
prod=1.+0.j
for i in range(1,nk-1):            # <evec_0|evec_1>...<evec_58|evec_59>
  prod*=np.vdot(evec[i-1],evec[i]) # a*=b means a=a*b

# now compute the phase factors needed for last inner product
orb=np.array([0.0,0.5])            # relative coordinates of orbitals
phase=np.exp((-2.j)*np.pi*orb)     # construct phase factors
evec_last=phase*evec[0]            # evec[60] constructed from evec[0]
prod*=np.vdot(evec[-2],evec_last)  # include <evec_59|evec_last>

print("Berry phase is %7.3f"% (-np.angle(prod)))

# -----------------------------------
# Berry phase via the wf_array method
# -----------------------------------

evec_array=wf_array(my_model,[61])       # set array dimension
evec_array.solve_on_grid([0.])           # fill with eigensolutions
berry_phase=evec_array.berry_phase([0])  # Berry phase of bottom band

print("Berry phase is %7.3f"% berry_phase)
