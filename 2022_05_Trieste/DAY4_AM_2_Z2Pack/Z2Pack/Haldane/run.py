import logging
import z2pack
import numpy as np
import matplotlib.pyplot as plt
import tbmodels as tbmodels

logging.getLogger('z2pack').setLevel(logging.WARNING)
    
def Haldane(M_rel,phase):
    # set model parameters
    t=-1.0
    M=M_rel*0.15
    t2 =0.15*np.exp((1.j)*phase)
    t2c=t2.conjugate()

    # define lattice vectors
    lat=[[1.0,0.0],[0.5,np.sqrt(3.0)/2.0]]
    # define coordinates of orbitals
    orb=[[1./3.,1./3.],[2./3.,2./3.]]

    model = tbmodels.Model(
        on_site=(-M,M),
        pos=orb,
        occ=1,
        uc=lat)

    model.add_hop(t, 0, 1, [ 0, 0])
    model.add_hop(t, 1, 0, [ 1, 0])
    model.add_hop(t, 1, 0, [ 0, 1])
    # add second neighbour complex hoppings
    model.add_hop(t2 , 0, 0, [ 1, 0])
    model.add_hop(t2 , 1, 1, [ 1,-1])
    model.add_hop(t2 , 1, 1, [ 0, 1])
    model.add_hop(t2c, 1, 1, [ 1, 0])
    model.add_hop(t2c, 0, 0, [ 1,-1])
    model.add_hop(t2c, 0, 0, [ 0, 1])
    
    return model

M=0.0
phase=np.pi/2
Haldane_model = Haldane(M,phase)
tb_system = z2pack.tb.System(Haldane_model)


settings = {
    'num_lines': 31,
    'pos_tol': 1e-2,
    'gap_tol': 0.2,
    'move_tol': 0.3,
    'iterator': range(10, 35, 12),
    'min_neighbour_dist': 2e-2
}

res = z2pack.surface.run(system=tb_system, surface=lambda s, t: [s, t], **settings)
z2pack.plot.wcc(res, gaps=False)
plt.savefig('Haldane_WCC.png', bbox_inches='tight')
print("The total Chern number is: ",z2pack.invariant.chern(res))     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
