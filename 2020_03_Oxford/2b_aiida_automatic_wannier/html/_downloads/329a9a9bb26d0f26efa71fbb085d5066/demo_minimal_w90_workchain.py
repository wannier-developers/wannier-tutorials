from aiida.engine import run
from aiida.orm import Str, Dict, KpointsData, StructureData, load_code
from aiida.plugins import WorkflowFactory

from aiida_wannier90.orbitals import generate_projections


pw_code=load_code("<CODE LABEL>")  # Replace with the QE pw.x code label
wannier_code=load_code("<CODE LABEL>")  # Replace with the Wannier90 wannier.x code label
pw2wannier90_code=load_code("<CODE LABEL>")  # Replace with the QE pw2wannier90.x code label
pseudo_family_name="<UPF FAMILY NAME>" # Replace with the name of the pseudopotential family for SSSP efficiency 


# GaAs structure
a = 5.68018817933178  # angstrom
structure = StructureData(
    cell=[[-a / 2., 0, a / 2.], [0, a / 2., a / 2.], [-a / 2., a / 2., 0]]
)
structure.append_atom(symbols=['Ga'], position=(0., 0., 0.))
structure.append_atom(symbols=['As'], position=(-a / 4., a / 4., a / 4.))

# 4x4x4 k-points mesh for the SCF
kpoints_scf = KpointsData()
kpoints_scf.set_kpoints_mesh([4, 4, 4])

# 10x10x10 k-points mesh for the NSCF/Wannier90 calculations
kpoints_nscf = KpointsData()
kpoints_nscf.set_kpoints_mesh([10, 10, 10])

# k-points path for the band structure
kpoint_path = Dict(dict={
    'point_coords': {
        'GAMMA': [0.0, 0.0, 0.0],
        'K': [0.375, 0.375, 0.75],
        'L': [0.5, 0.5, 0.5],
        'U': [0.625, 0.25, 0.625],
        'W': [0.5, 0.25, 0.75],
        'X': [0.5, 0.0, 0.5]
    },
    'path': [('GAMMA', 'X'), ('X', 'U'), ('K', 'GAMMA'),
             ('GAMMA', 'L'), ('L', 'W'), ('W', 'X')]
})

# sp^3 projections, centered on As
projections = generate_projections(
    [
        {
            'position_cart' :(-a / 4., a / 4., a / 4.),
            'ang_mtm_l_list': -3,
            'spin': None,
        },
    ],
    structure=structure
)

# Load the workflow
MinimalW90WorkChain = WorkflowFactory('wannier90.minimal')

# Run the workflow
run(
    MinimalW90WorkChain,
    pw_code=pw_code,
    wannier_code=wannier_code,
    pw2wannier90_code=pw2wannier90_code,
    pseudo_family=Str(pseudo_family_name),
    structure=structure,
    kpoints_scf=kpoints_scf,
    kpoints_nscf=kpoints_nscf,
    kpoint_path=kpoint_path,
    projections=projections
)
