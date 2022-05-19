#!/usr/bin/env python
from __future__ import print_function # python3 style print

from pythtb import * # import TB model class
import matplotlib.pyplot as plt

# set geometry
lat=[[1.0,0.0],[0.0,1.0]]
orb=[[0.0,0.0],[0.5,0.5]]
my_model=tbmodel(2,2,lat,orb)

# set model
Delta  = 5.0
t_0    = 1.0
tprime = 0.4
my_model.set_sites([-Delta,Delta])
my_model.add_hop(-t_0, 0, 0, [ 1, 0])
my_model.add_hop(-t_0, 0, 0, [ 0, 1])
my_model.add_hop( t_0, 1, 1, [ 1, 0])
my_model.add_hop( t_0, 1, 1, [ 0, 1])
my_model.add_hop( tprime   , 1, 0, [ 1, 1])
my_model.add_hop( tprime*1j, 1, 0, [ 0, 1])
my_model.add_hop(-tprime   , 1, 0, [ 0, 0])
my_model.add_hop(-tprime*1j, 1, 0, [ 1, 0])
my_model.display()

# generate k-point path and labels and solve Hamiltonian
path=[[0.0,0.0],[0.0,0.5],[0.5,0.5],[0.0,0.0]]
k_lab=(r'$\Gamma $',r'$X$', r'$M$', r'$\Gamma $')
(k_vec,k_dist,k_node)=my_model.k_path(path,121)
evals=my_model.solve_all(k_vec)

# plot band structure
fig, ax = plt.subplots(figsize=(4.,3.))
ax.set_xlim([0,k_node[-1]])
ax.set_xticks(k_node)
ax.set_xticklabels(k_lab)
for n in range(len(k_node)):
  ax.axvline(x=k_node[n], linewidth=0.5, color='k')
ax.plot(k_dist,evals[0],color='k')
ax.plot(k_dist,evals[1],color='k')
fig.savefig("checkerboard_bsr.pdf")
