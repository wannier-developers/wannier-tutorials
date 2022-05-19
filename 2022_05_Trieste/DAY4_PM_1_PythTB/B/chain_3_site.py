#!/usr/bin/env python
from __future__ import print_function # python3 style print

# Chain with three sites per cell

from pythtb import *
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

# construct the model
t=-1.3
delta=2.0
lmbd=0.3
my_model=set_model(t,delta,lmbd)

# compute the results on a uniform k-point grid
evec_array=wf_array(my_model,[21])       # set array dimension
evec_array.solve_on_grid([0.])           # fill with eigensolutions

# obtain Berry phases and convert to Wannier center positions
#   constrained to the interval [0.,1.]
wfc0=evec_array.berry_phase([0])/(2.*np.pi)%1.
wfc1=evec_array.berry_phase([1])/(2.*np.pi)%1.
x=evec_array.berry_phase([0,1],berry_evals=True)/(2.*np.pi)%1.
gwfc0=x[0]
gwfc1=x[1]

print ("Wannier centers of bands 0 and 1:")
print(("  Individual"+" Wannier centers: "+2*"%7.4f") % (wfc0,wfc1))
print(("  Multiband "+" Wannier centers: "+2*"%7.4f") % (gwfc1,gwfc0))
print()

# construct and solve finite model by cutting 10 cells from infinite chain
finite_model=my_model.cut_piece(10,0)
(feval,fevec)=finite_model.solve_all(eig_vectors=True)

print ("Finite-chain eigenenergies associated with")
print(("Band 0:"+10*"%6.2f")% tuple(feval[0:10]))
print(("Band 1:"+10*"%6.2f")% tuple(feval[10:20]))

# find maxloc Wannier centers in each band subspace
xbar0=finite_model.position_hwf(fevec[0:10,],0)
xbar1=finite_model.position_hwf(fevec[10:20,],0)
xbarb=finite_model.position_hwf(fevec[0:20,],0)

print ("\nFinite-chain Wannier centers associated with band 0:")
print((10*"%7.4f")% tuple(xbar0))
x=10*(wfc0,)
print(("Compare with bulk:\n"+10*"%7.4f")% x)
print ("\nFinite-chain Wannier centers associated with band 1:")
print((10*"%7.4f")% tuple(xbar1))
x=10*(wfc1,)
print(("Compare with bulk:\n"+10*"%7.4f")% x)
print ("\nFirst 10 finite-chain Wannier centers associated with bands 0 and 1:")
print((10*"%7.4f")% tuple(xbarb[0:10]))
x=5*(gwfc0,gwfc1)
print(("Compare with bulk:\n"+10*"%7.4f")% x)
