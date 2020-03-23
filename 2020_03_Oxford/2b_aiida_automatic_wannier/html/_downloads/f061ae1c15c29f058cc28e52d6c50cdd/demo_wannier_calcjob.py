#!/usr/bin/env runaiida
from aiida.engine import submit
from aiida.orm import load_node, Code, Dict

code = Code.get_from_string("<CODE LABEL>")  # REPLACE <CODE LABEL>

# Fill in here the PK of the *primitive* structure that you obtained
# in the tutorial. If you want to reuse the crystal structure that
# was already imported, you can use instead the following UUID: '8c108d56-aca6-43f6-baa6-94f7d1d9887d'
structure = load_node(<PK>)
# Here, we are reusing the same k-points used in the NSCF step.
# Exercise: load this node in the `verdi shell`, and then use
# `kpoints.get_kpoints()` to check the full list of kpoints.
kpoints = load_node('d4d4e086-af7a-46c7-b7a0-9c5c2c9dfc7b')

## Main Wannier run
do_preprocess = False
## This is the node that we imported, discussed in the tutorial
parent_folder = load_node('71155a0b-6cb9-4712-a043-dc4798ccfaaf')

## Note: if you wanted to run a pre-process step (`Wannier90.x -pp`),
## than you would replace the two lines above with the following one:
#do_preprocess = True



parameters = Dict(
    dict={
        'bands_plot': True,
        'num_iter': 300,
        'guiding_centres': True,
        'num_wann': 4,
        'mp_grid': [4,4,4],
        'exclude_bands': [1, 2, 3, 4, 5]
    }
)

kpoint_path = Dict(
    dict={
        'point_coords': {
            'GAMMA': [0.0, 0.0, 0.0],
            'L': [0.5, 0.5, 0.5],
            'X': [0.5, 0.0, 0.5]
        },
        'path': [('L', 'GAMMA'), ('GAMMA', 'X')]
    }
)

projections = List()
projections.extend(['As:s','As:p'])

# Settings node, with additional configuration
settings_dict = {}
if do_preprocess:
    settings_dict.update(
        {'postproc_setup': True}
    )  

# Prepare the builder to launch the calculation
builder = code.get_builder()
builder.metadata.options.max_wallclock_seconds = 30 * 60  # 30 min
builder.metadata.options.resources = {"num_machines": 1}

builder.structure = structure
builder.projections = projections
builder.parameters = parameters
builder.kpoints = kpoints
builder.kpoint_path = kpoint_path
if not do_preprocess:
    builder.local_input_folder = parent_folder
builder.settings = Dict(dict=settings_dict)

# Run the calculation and get both the results and the node
calcjobnode = submit(builder)

print("CalcJobNode: {}".format(calcjobnode))
print("Use `verdi process list` or `verdi process show {}` to check the progress".format(calcjobnode.pk))

