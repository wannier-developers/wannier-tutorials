#!/usr/bin/env runaiida
import os
import sys

from ase.io import read as aseread

from aiida import orm
from aiida.engine import submit

from aiida_wannier90_workflows.workflows import Wannier90BandsWorkChain

# Code labels for `pw.x`, `pw2wannier90.x`, `projwfc.x`, and `wannier90.x`.
# Change these according to your aiida setup.
codes = {
    "pw": "qe-pw-6.8@localhost",
    "projwfc": "qe-projwfc-6.8@localhost",
    "pw2wannier90": "qe-pw2wannier90-6.8@localhost",
    "wannier90": "wannier90-3.1@localhost",
}

# Filename of a structure.
# filename = "GaAs.xsf"
if len(sys.argv) != 2:
    print(f"Please pass a filename for a structure as the argument.")
    sys.exit(1)
filename = sys.argv[1]
if not os.path.exists(filename):
    print(f"{filename} not existed!")
    sys.exit(1)

# Read a structure file and store as an `orm.StructureData`.
structure = orm.StructureData(ase=aseread(filename))
structure.store()
print(f"Read and stored structure {structure.get_formula()}<{structure.pk}>")

# Prepare the builder to launch the workchain.
# We use fast protocol to converge faster.
builder = Wannier90BandsWorkChain.get_builder_from_protocol(
    codes,
    structure,
    protocol="fast",
)

# Submit the workchain.
workchain = submit(builder)
print(f"Submitted {workchain.process_label}<{workchain.pk}>")

print(
    "Run any of these commands to check the progress:\n"
    f"verdi process report {workchain.pk}\n"
    f"verdi process show {workchain.pk}\n"
    "verdi process list\n"
)
