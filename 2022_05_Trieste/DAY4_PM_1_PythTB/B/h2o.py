#!/usr/bin/env python
from __future__ import print_function # python3 style print

# ----------------------------------------------------------
# Tight-binding model for H2O molecule
# ----------------------------------------------------------

# import the pythtb module
from pythtb import *
import numpy as np

# geometry: bond length and half bond-angle
b=1.0; angle=54.0*np.pi/180

# site energies [O(s), O(p), H(s)]
eos=-1.5; eop=-1.2; eh=-1.0

# hoppings [O(s)-H(s), O(p)-H(s)]
ts=-0.4; tp=-0.3

# define frame for defining vectors: 3D Cartesian
lat=[[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]]

# define coordinates of orbitals: O(s,px,py,pz) ; H(s) ; H(s)
orb=[ [0.,0.,0.], [0.,0.,0.], [0.,0.,0.], [0.,0.,0.],
      [b*np.cos(angle), b*np.sin(angle),0.],
      [b*np.cos(angle),-b*np.sin(angle),0.] ]

# define model
my_model=tbmodel(0,3,lat,orb)
my_model.set_onsite([eos,eop,eop,eop,eh,eh])
my_model.set_hop(ts,0,4)
my_model.set_hop(ts,0,5)
my_model.set_hop(tp*np.cos(angle),1,4)
my_model.set_hop(tp*np.cos(angle),1,5)
my_model.set_hop(tp*np.sin(angle),2,4)
my_model.set_hop(-tp*np.sin(angle),2,5)

# print model
my_model.display()

# solve model
(eval,evec)=my_model.solve_all(eig_vectors=True)

# the model is real, so OK to discard imaginary parts of eigenvectors
evec=evec.real

# optional: choose overall sign of evec according to some specified rule
# (here, we make the average oxygen p component positive)
for i in range(len(eval)):
  if sum(evec[i,1:4]) < 0:
    evec[i,:]=-evec[i,:]

# print results, setting numpy to format floats as xx.xxx
np.set_printoptions(formatter={'float': '{: 6.3f}'.format})
# print eigenvalues and real parts of eigenvectors, one to a line
print("  n   eigval   eigvec")
for n in range(6):
    print(" %2i  %7.3f  " % (n,eval[n]), evec[n,:])
