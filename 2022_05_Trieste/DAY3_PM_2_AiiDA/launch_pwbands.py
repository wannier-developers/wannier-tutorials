#!/usr/bin/env runaiida
import os
import sys

from ase.io import read as aseread

from aiida import orm
from aiida.engine import submit

from aiida_quantumespresso.workflows.pw.bands import PwBandsWorkChain

# Code labels for `pw.x`
# Change these according to your aiida setup.
code = "qe-pw-6.8@localhost"

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
builder = PwBandsWorkChain.get_builder_from_protocol(
    code,
    structure,
    protocol="fast",
)
builder.pop("relax", None)

# Submit the workchain.
workchain = submit(builder)
print(f"Submitted {workchain.process_label}<{workchain.pk}>")

print(
    "Run any of these commands to check the progress:\n"
    f"verdi process report {workchain.pk}\n"
    f"verdi process show {workchain.pk}\n"
    "verdi process list\n"
)
