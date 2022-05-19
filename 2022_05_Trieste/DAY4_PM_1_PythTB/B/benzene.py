#!/usr/bin/env python
from __future__ import print_function # python3 style print

# ----------------------------------------------------------
# Tight-binding model for p_z states of benzene molecule
# ----------------------------------------------------------

from pythtb import *

# set up molecular geometry
lat=[[1.0,0.0],[0.0,1.0]]        # define coordinate frame: 2D Cartesian
r=1.2                            # distance of atoms from center
orb=np.zeros((6,2),dtype=float)  # initialize array for orbital positions
for i in range(6):               # define coordinates of orbitals
  angle=i*np.pi/3.0
  orb[i,:]= [r*np.cos(angle), r*np.sin(angle)]

# set site energy and hopping amplitude, respectively
ep=-0.4
t=-0.25

# define model
my_model=tbmodel(0,2,lat,orb)
my_model.set_onsite([ep,ep,ep,ep,ep,ep])
my_model.set_hop(t,0,1)
my_model.set_hop(t,1,2)
my_model.set_hop(t,2,3)
my_model.set_hop(t,3,4)
my_model.set_hop(t,4,5)
my_model.set_hop(t,5,0)

# print model
my_model.display()

# solve model and print results
(eval,evec)=my_model.solve_all(eig_vectors=True)

# print results, setting numpy to format floats as xx.xxx
np.set_printoptions(formatter={'float': '{: 6.3f}'.format})
# Print eigenvalues and real parts of eigenvectors, one to a line
print("  n   eigval   eigvec")
for n in range(6):
    print(" %2i  %7.3f  " % (n,eval[n]), evec[n,:].real)
