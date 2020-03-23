#!/usr/bin/env runaiida
import sys
from aiida.orm import StructureData, Bool, Code, Dict
from aiida.engine import submit
from ase.io import read as aseread
from aiida_wannier90_workflows.workflows import Wannier90BandsWorkChain

# Codenames for pw.x, pw2wannier90.x, projwfc.x and wannier90.x
# Please modify these according to your machine
pw_code = Code.get_from_string("<CODE LABEL>")  # e.g. 'qe-6.5-pw@localhost'
pw2wan_code = Code.get_from_string("<CODE LABEL>")  # e.g. 'qe-6.5-pw2wannier90@localhost'
projwfc_code = Code.get_from_string("<CODE LABEL>")  # e.g. 'qe-6.5-projwfc@localhost'
wan_code = Code.get_from_string("<CODE LABEL>")  # e.g. 'wannier90-3.1.0-wannier@localhost'

# The 1st commandline argument specifies the structure to be calculated
xsf_file = sys.argv[1]  # e.g. 'CsH.xsf'

# Read xsf file and convert into a stored StructureData
structure = StructureData(ase=aseread(xsf_file))

# Prepare the builder to launch the workchain
builder = Wannier90BandsWorkChain.get_builder()
builder.structure = structure
builder.code = {
    'pw': pw_code,
    'pw2wannier90': pw2wan_code,
    'projwfc': projwfc_code,
    'wannier90': wan_code
}
# For this tutorial, we are using the 'testing' protocol,
# with all cutoffs halved, to speed up the simulations
builder.protocol = Dict(dict={'name': 'testing'})
# Flags to control the workchain behaviour
builder.controls = {
    # If True, compute only valence bands (NB: use for insulators only!)
    'only_valence': Bool(False),
    # If True, perform maximal-localisation (MLWF) procedure, i.e., minimise the spread Omega
    'do_mlwf': Bool(True),
}

# Submits the workchain
workchain = submit(builder)

print('launched WorkChain<{}> for structure {}'.format(workchain.pk, structure.get_formula()))
print("Use `verdi process list` or `verdi process show {}` to check the progress".format(workchain.pk))
