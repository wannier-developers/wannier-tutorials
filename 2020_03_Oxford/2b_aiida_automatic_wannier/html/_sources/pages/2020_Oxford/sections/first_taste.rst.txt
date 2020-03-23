A first taste of AiiDA
======================

Let's start with a quick demo of how AiiDA can make your life easier as a computational scientist.

We'll be using the ``verdi`` command-line interface,
which lets you manage your AiiDA installation, inspect the contents of your database,  control running calculations and more.

As the first thing, open a terminal and type ``workon aiida`` to enter the "virtual environment" where AiiDA is installed.
You will know that you are in the virtual environment because each new line will start with ``(aiida)``, e.g.::

  (aiida) max@qmobile:~$

Note that you will need to retype ``workon aiida`` every time you open a new terminal.

Here are some first tasks for you:

 * The ``verdi`` command supports **tab-completion**:
   In the terminal, type ``verdi``, followed by a space and press the 'Tab' key twice to show a list of all the available sub commands.
 * For help on ``verdi`` or any of its subcommands, simply append the ``--help/-h`` flag:

   .. code:: bash

       verdi -h

.. note:: This tutorial is a short crash course into AiiDA, focusing on
   `Wannier90`_ as the code that AiiDA will run (via the `aiida-wannier90`_
   plugin). 

   Many more codes are supported by AiiDA (see full updated list of plugins on
   the `AiiDA plugin registry`_).
   If you want to see a similar first-taste tutorial, but focused on `Quantum ESPRESSO`_
   instead (using the `aiida-quantumespresso`_ plugin), you can check the
   :ref:`"first-taste" page of the tutorial held in Ljubiana (2019) <Ljubliana 2019 first taste>`.

.. _Wannier90: http://www.wannier.org
.. _aiida-wannier90: https://github.com/aiidateam/aiida-wannier90
.. _AiiDA plugin registry: https://aiidateam.github.io/aiida-registry/
.. _Quantum ESPRESSO: https://www.quantum-espresso.org
.. _aiida-quantumespresso: https://github.com/aiidateam/aiida-quantumespresso


Importing a crystal structure from a file
-----------------------------------------

We will use a gallium arsenide (GaAs) primitive cell with 2 atoms in this
first part of the tutorial.

We provide the crystal structure, in `XSF format`_, here: 
:download:`GaAs.xsf<include/xsf/GaAs.xsf>`.

.. _XSF format: http://www.xcrysden.org/doc/XSF.html

You can download the file in a folder in the virtual machine,
and then import it into AiiDA (via the `ASE`_ library)
using the following ``verdi`` command, run from a bash shell:

.. _ASE: https://wiki.fysik.dtu.dk/ase/

.. code:: bash

    verdi data structure import ase GaAs.xsf

Each piece of data in AiiDA gets a PK number (a "primary key")
that identifies it in your database.
This is printed out on the screen by the ``verdi data structure import`` command.
Mark it down, as we are going to use it in the next commands.

.. note::

   In the next commands, replace the string ``<PK>`` with the appropriate PK number.

Let us first inspect the node you just created:

.. code:: bash

    verdi node show <PK>

You will get in output some information on the node,
including its type (``StructureData``, the AiiDA data type for storing crystal 
structures), a label and a description (empty for now, can be changed), 
a creation time (``ctime``) and a last modification time (``mtime``), 
the PK of the node and its UUID (universally unique identifier).

.. note::

  **When should I use the PK and when should I use the UUID?**

  A **PK** is a short integer identifying the node and therefore easy to remember. 
  However, the same PK number (e.g., PK=10)
  might appear in two different databases referring to two completely different
  pieces of data.

  A **UUID** is a hexadecimal string that might look like this::

     d11a4829-3e19-4978-bfcf-c28ddeb0891e

  A UUID has instead the nice feature to be globally unique: even if you export
  your data and a colleague imports it, the UUIDs will remain the same
  (while the PKs will typically be different).

  Therefore, use the UUID to keep a long-term reference to a node.
  Feel free to use the PK for quick, everyday use (e.g. to inspect a node).

.. note:: 
  All AiiDA commands accepting a PK can also accept a UUID. Check this by
  trying the command above, this time with ``verdi node show <UUID>``.

  Note the following:

  - AiiDA does not require the full UUID, but just the first part of it,
    as long as only one node starts with the string you provide. E.g., in the example above,
    you could also say ``verdi node show d11a4829-3e19``. Most probably, instead,
    ``verdi node show d1`` will return an error, since you might
    have more than one node starting with the string ``d1``.

  - By default, if you pass a valid integer, AiiDA will assume it is a PK;
    if at least one of the characters is not a digit, then AiiDA will assume
    it is (the first part of) a UUID.

  - How to solve the issue, then, when the first part of the UUID is composed only by
    digits (e.g. in ``2495301c-dd00-42d6-92e4-1a8c171bbb4a``)? As described above, using
    ``verdi node show 24953`` would look for a node with ``PK=24953``. As a solution,
    just add a dash, e.g. ``verdi node show 24953-`` so that AiiDA will consider
    this as the beginning of the UUID.

    Note that you can put the dash in any part of the string, and you don't need
    to respect the typical UUID pattern with 8-4-4-4-12 characters per section:
    AiiDA will anyway first strip all dashes, and then put them back in the right
    place, so e.g. ``verdi node show 24-95-3`` will give you the same result as 
    ``verdi node show 24953-``.

- Try to use again ``verdi node show`` on the ``StructureData`` node above,
  just with the first part of the UUID (that you got from the first call to
  ``verdi node show`` above).


Running a job calculation
-------------------------

Introduction and importing existing simulations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In AiiDA, one very important type of calculation is called "calculation job" (whose logic is 
implemented in a ``CalcJob`` python class, and that is stored upon execution using a ``CalcJobNode`` python class).
These calculations represent the execution
of an external code (e.g. Quantum ESPRESSO, Wannier90, ...), very often on a different computer
than the one where AiiDA is installed.
The execution is automatically tracked by AiiDA (input creation, submission, waiting for the job scheduler,
file retrieval and parsing) and its inputs and outputs are connected to the ``CalcJobNode`` (representing
the execution) via INPUT and CREATE links.

In the following, we want to launch a ``CalcJob`` running a Wannier90 calculation.
Typically, before running a Wannier90 calculation, you need to obtain the ``.amn``, ``.mmn``, ... files
from the interface to a first-principles code. In order to keep this tutorial focused on Wannier90, we have
already run that part with AiiDA (using Quantum ESPRESSO) and we will just import it into your database.

To achieve so, download this AiiDA export file: 
:download:`example-gaas-wannier.aiida <../../../assets/2020_Oxford/example-gaas-wannier.aiida>`
and, once you have downloaded it in the current folder, run the following command in your bash shell:

.. code:: bash

   verdi import example-gaas-wannier.aiida

This will import, in particular, the node with UUID ``71155a0b-6cb9-4712-a043-dc4798ccfaaf``,
that contains the ``.amn``, ``.mmn``, ... files created by the ``pw2wannier90.x`` code of Quantum ESPRESSO.
Its provenance looks like the following figure (with some output nodes of the calculations not shown for clarity):

.. _fig oxford2020 folderdata_provenance:

.. figure:: include/images/folderdata_provenance.png
   :width: 100%

   Provenance graph for the ``FolderData`` node (``71155a0b``) that we have already run. At the top, we see the execution
   of a ``get_primitive()`` calc function (described later in :ref:`the appendix<Oxford 2020 appendix get_primitive>`)
   to obtain a primitive cell from a conventional cell.
   The darker red rectangles represent the various calc jobs that we have run
   for you, in particular:

   - the Quantum ESPRESSO SCF step (UUID ``dcd4c286``)
   - the Quantum ESPRESSO NSCF step (UUID ``be52abbf``)
   - the Wannier90 preprocess (``-pp``) step (UUID ``a95261e2``)
   - the Quantum ESPRESSO pw2wannier90 step (UUID ``d34d62f9``).

**Exercise**: To check that the import worked correctly, use ``verdi node show`` on the UUID of the ``FolderData``
mentioned above to check that you indeed have the node in your database.

**Exercise**: ``FolderData`` is a type of node that stores an arbitrary set of files and folders in AiiDA.
Check the list of files included in it with the command ``verdi node repo ls 71155a0b``, and check the content of
a given file (e.g. the ``aiida.mmn`` file) with ``verdi node repo cat 71155a0b aiida.mmn``.

**Exercise**: In the figure above, verify that all calculations are connected between them via provenance links (through
some data node). Try to understand how, e.g., the NSCF calculation "restarts" from the SCF via a ``RemoteData`` node
(that represents a reference to the folder in the computational cluster where the SCF calculation was run), or how the 
pw2wannier90 step uses as input both the ``RemoteData`` node of the NSCF and the ``.nnkp`` file generated by ``wannier90.x -pp``.

Running Wannier90 with AiiDA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following python script sets up all inputs to run the Wannier90 code. We will discuss relevant parts below; we will
first launch it so that we can analyze its output while it runs.

.. literalinclude:: include/snippets/demo_wannier_calcjob.py

Download the :download:`demo_wannier_calcjob.py <include/snippets/demo_wannier_calcjob.py>` script to your working directory.
It contains a few placeholders for you to fill in:

#. the VM already has a number of codes preconfigured. Use ``verdi code list`` to find the label for the Wannier90
   code and use it in the script. Note: *do not use the imported code*, as the computer on which it runs will not
   be configured by default.
#. replace the PK of the structure with the one you obtained earlier (*important*: use the PK of the *primitive* structure).

Then submit the calculation using:

.. code:: bash

    verdi run demo_wannier_calcjob.py

From this point onwards, the AiiDA daemon will take care of your calculation: creating the necessary input files, running the calculation, and parsing its results.

In order to be able to do this, the AiiDA daemon must be running: to check this, you can run the command:

.. code:: bash

    verdi daemon status

and, if the daemon is not running, you can start it with

.. code:: bash

    verdi daemon start

It should take less than one minute to complete.

Analyzing the outputs of a calculation
--------------------------------------

Let's have a look at how your calculation is doing:

.. code:: bash

   verdi process list  # shows only running processes
   verdi process list --all  # shows all processes

Again, your calculation will get a PK, which you can use to get more information on it:

.. code:: bash

   verdi process show <PK>

As you can see, AiiDA has tracked all the inputs provided to the calculation, allowing you (or anyone else) to reproduce it later on.
AiiDA's record of a calculation is best displayed in the form of a provenance graph:

.. figure:: include/images/demo_wannier_calc.png
   :width: 100%

   Provenance graph for a single Wannier90 calculation.

You can generate such a provenance graph for any calculation or data in AiiDA by running:

.. code:: bash

  verdi node graph generate <PK>

Try to reproduce the figure using the PK of your calculation (note that in our figure, we have used the
``--ancestor-depth=1`` option of ``verdi node graph generate`` to only show direct inputs; if you don't, you will see
also the full provenance of the data, similar to the previous figure shown earlier).

You might wonder what happened under the hood, e.g. where to find the actual input and output files of the calculation.
You will learn more about this in some of the advanced tutorials on AiiDA -- for now, here are a few useful commands:

.. code:: bash

   verdi calcjob inputcat <PK>  # shows the input file of the calculation
   verdi calcjob outputcat <PK>  # shows the output file of the calculation
   verdi calcjob res <PK>  # shows the parsed output

**Exercise**: Here are a few questions you can now answer using these commands (try to check both the raw output and the parsed output)
 * What are the values of the various components of the spread :math:`\Omega_I`, :math:`\Omega_D`, :math:`\Omega_{OD}`?
 * How many Wannier functions have been computed?
 * Was there any warning?

Understanding the launcher script
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Above, we have just provided you a script that submits a calculation. 
Let us now check in detail some relevant sections, and how the input information
got converted into the Wannier90 raw input file.

Choosing a structure
********************
In this simple example, we load a structure already stored in the AiiDA database
(it is the one we imported from a file earlier on).
We do this using the ``load_node`` command (that accepts
either an integer PK or a string UUID).

Choosing the k-points
*********************
Also for ``kpoints``, we are loading these from file. The reason is that we
already executed the Quantum ESPRESSO NSCF run, and we need to be sure that the order
of the k-points is the same (exercise: check in :numref:`fig oxford2020 folderdata_provenance` that the 
``KpointsData`` node that we are using is indeed the input ``KpointsData``
of the NSCF calculation). Otherwise, one can create an AiiDA ``KpointsData``
and use the ``set_kpoints`` method to pass a :math:`N\times 3` numpy array, 
where :math:`N` is the number of k-points.

Setting up input parameters
***************************
One very important input node is the ``parameters`` node, containing the input
flags for the code.

.. code:: python

   parameters = Dict(
      dict={
         'bands_plot': True,
         ...
      })

In particular, ``parameters`` is a ``Dict`` node, i.e.,
an AiiDA node containing a dictionary of key-value pairs (stored in the AiiDA
database and that can be easily queried - we will not see how to run queries in this
tutorial, but you can check the `AiiDA documentation on querying`_ or the :ref:`full tutorial <querybuilder>`
for more information on this).

.. _AiiDA documentation on querying: https://aiida.readthedocs.io/projects/aiida-core/en/v1.1.1/working_with_aiida/index.html#querying-data

**Exercise**: Use ``verdi calcjob inputcat <PK>`` (using the ``PK`` of the calc job)
and check how the information in the ``parameters`` has been converted
into the Wannier90 input file.

Setting up the projections
**************************

In ``aiida-wannier90``, there are two ways to set up ``projections``.
Here, we are using the simplest approach (i.e., a list of strings, that are simply
inserted in the corresponding section of the raw input file). Similarly to a ``Dict`` node,
these strings are wrapped in a ``List`` AiiDA node, so that it gets stored and are queryable.

We will see a second (more easily queryable) way later on during this tutorial.

Setting up an (optional) list of k-points for the band plot
***********************************************************

The path to compute an (interpolated) band structure needs to be specified
as a ``Dict`` node, contianing two keys: ``point_coords`` (a dictionary
with high-symmetry point labels and coordinates), and a ``path``
(a list of pairs of labels, to indicate band-path segments):

.. code:: python

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

**Exercise**: Check how this has been converted into the raw input file.

Setting up the (optional) calculation settings
**********************************************
While often you don't need to specify additional control parameters, there
are cases in which you want to specify additional options to tune 
the way AiiDA will run the code.

You can find the full documentation of accepted keys for the ``settings``
in the `aiida-wannier90 documentation`_ (e.g. to specify random projections,
or to retrieve/not retrieve specific files at the end of the run).

.. _aiida-wannier90 documentation: https://aiida-wannier90.readthedocs.io/en/v2.0.0/inputexample.html#settings

One important option that you will use very often is the flag ``postproc_setup``:
if set to ``True``, it will run a Wannier90 post-processing run (i.e., ``wannier90.x -pp``).

In our case, ``do_preprocess`` is ``False`` so this is not set, but you would need
to run it in a full calculation including a DFT code.

.. code:: python

   # Settings node, with additional configuration
   settings_dict = {}
   if do_preprocess:
      settings_dict.update(
         {'postproc_setup': True}
      )  


Setting up all inputs in a builder
**********************************
Once you have created the nodes or loaded them from 
the database, you need to prepare a calculation, connect all inputs and then run
(or submit it).

This is done creating a new calculation ``builder`` from a code: ``builder = code.get_builder()``.
Then, all inputs are attached to the builder as follows:

.. code:: python

   builder.structure = structure
   builder.projections = projections
   builder.parameters = parameters
   ...

Finally, you can:

- ``run`` the calculation (this stops the interpreter at that line, until the simulation
  is done, and then the execution of the python script continues):
  
    .. code:: python

      from aiida.engine import run
      results = run(builder)

  At the end, you will get a dictionary of ``results``, one for every output node.

- If you want to run the calculation, but also get a reference to the
  ``CalcJobNode`` that represents the execution, you can use instead:
  
    .. code:: python

      from aiida.engine import run_get_node
      results, calcjobnode = run_get_node(builder)

- If you want to submit to the daemon (what is done in the example above),
  you can use instead:

    .. code:: python

      from aiida.engine import submit
      calcjobnode = submit(builder)

  In this case, you just get immediately a reference to the ``CalcJobNode`` 
  (not yet completed) and you can continue with the execution of the python script.
  This is useful e.g. if you want to submit many independent calculations at once
  in a ``for`` loop, and then let them run in parallel.


From calculations to workflows
------------------------------

AiiDA can help you run individual calculations but it is really designed to help you run workflows that involve several calculations, while automatically keeping track of the provenance for full reproducibility.

As the final step, we are going to launch the ``MinimalW90WorkChain`` workflow, a demo workflow
shipped with the ``aiida-wannier90`` plugin, that also takes care of running the preliminary DFT
steps using Quantum ESPRESSO.

Here is a submission script that we are going to use:

.. literalinclude:: include/snippets/demo_minimal_w90_workchain.py

Download the :download:`demo_bands.py <include/snippets/demo_minimal_w90_workchain.py>` snippet.
You will need to edit the first lines, specifying the name of the AiiDA codes for Quantum ESPRESSO executables
``pw.x`` and ``pw2wannier90.x``, and for the Wannier90 code (that you can discover
as usual with ``verdi code list``).

Moreover, you need to specify which pseudopotentials you want to use. AiiDA comes with tools to manage
pseudopotentials in UPF format (the format used by Quantum ESPRESSO and a few more codes), and to group them
in "pseudopotential families". You can list all existing ones with ``verdi data upf listfamilies``. We want
to use the `SSSP library version 1.1 <https://www.materialscloud.org/discover/sssp/table/efficiency>`_.
Find the family you want to use and specify its name in the appropriate variable.

**Exercise**: Inspect the rest of the script to see how we are specifying inputs. 
In particular:

- Note how you can define a crystal structure directly in AiiDA, without using any external
  library, if you know the cell vectors and the atoms coordinates.

- Note how you can define a ``KpointsData`` node (``kpoints_scf``) that does not
  include an explicit list of k-points, but rather represents a regular grid (:math:`4\times4\times4`
  in this example, and similarly :math:`10\times10\times10` for ``kpoints_nscf``).
  The workflow, internally, knows that for the NSCF step one needs to unfold this k-points
  grid in an explicit grid of all k-points.

- Note a different way to specify the projections, using a more declarative format as a list of
  projection declarations (that gets internally converted in a queryable ``OrbitalData``,
  rather than just a list of strings).
  The documentation of the ``get_projections`` function and its parameters
  can be found `here <https://aiida-wannier90.readthedocs.io/en/v2.0.0/reference.html#aiida_wannier90.orbitals.generate_projections>`_.

Once you have saved your changes, you can run the workflow with:

.. code:: bash

  verdi run demo_minimal_w90_workchain.py

This workflow will:

  #. Run a SCF simulation on GaAs
  #. Run an NSCF calculation on a denser grid (with an explicit list of k-points)
  #. Run a post-process Wannier90 ``-pp`` calculation to get the ``.nnkp`` file
  #. Run the interface code ``pw2wannier90.x``
  #. Run the Wannierisation step, returning the interpolated bands.

The workflow should take ~5 minutes on a typical laptop.
You may notice that ``verdi process list`` now shows more than one entry.
While you wait for the workflow to complete, let's start exploring its provenance.

The full provenance graph obtained from ``verdi node graph generate`` will already be rather complex (you can try!),
so let's try browsing the provenance interactively instead.

In a new verdi shell, start the AiiDA REST API:

.. code:: bash

  verdi restapi

and open the |provenance browser| (from the browser inside the virtual machine).

.. |provenance browser| raw:: html

   <a href="https://www.materialscloud.org/explore/ownrestapi?base_url=http://127.0.0.1:5000/api/v4" target="_blank">Materials Cloud provenance browser</a>


.. note::
   
   The provenance browser is a Javascript application provided by Materials Cloud that connects to your AiiDA REST API.
   *Your data never leave your computer*.

Browse your AiiDA database.

 * Start by finding your workflow (in the left menu, filter the nodes by selecting
   ``Process -> Workflow -> WorkChain``.
   WorkChains are a specific type of workflows in AiiDA that allow to define multiple steps and can be paused
   and restarted between steps).

 * Inspect the inputs and returned outputs of the workflow in the provenance browser (outputs will appear once
   the calculations are done). Moreover, you can inspect the calculations that the workflow launched, and check both
   their input and output nodes (via the provenance browser), as well as the raw inputs and outputs of the calculation
   (in the page of a specific ``CalcJobNode``).

.. note:: 

     When perfoming calculations for a research project, at the end upon publication you can export your provenance graph using ``verdi export create`` and upload it to the `Materials Cloud Archive <https://archive.materialscloud.org/>`_, enabling your peers to explore the provenance of your calculations.

Once the workchain is finished, use ``verdi process show <PK>`` to inspect the ``MinimalW90WorkChain`` and find the PK of its ``interpolated_bands`` output.
Use this to produce an ``xmgrace`` output of the interpolated band structure:

.. code:: bash

   verdi data bands export --format agr --output wannier_bands.agr <PK>

that you can then visualise using ``xmgrace wannier_bands.agr``.


How to continue from here
-------------------------

The following appendix to this chapter discusses a bit more in detail
how to import and export crystal structures from an AiiDA database, and which
tools exist to obtain the primitive structure from a conventional structure,
or more generally from a supercell.

Importantly, the conversion of a crystal structure (conventional cell)
to a primitive cell means the creation of a Data node from another Data node
using a python function. The appendix shows how easy it is with AiiDA to
wrap python functions into AiiDA's ``calcfunctions`` that automatically 
preserve the provenance of the data transformation in the AiiDA graph.

If you do not have time right now, you can
:ref:`jump directly to the next tutorial section <Oxford 2020 autowannier>`,
where we will see how to use fully automated AiiDA workflows that can obtain
Wannier functions of a material with minimal input, without the need
to specifying input parameters apart from the crystal structure and the
code to run (and where even the choice of initial projections is automated).

.. _Oxford 2020 appendix get_primitive:

Appendix: Get the primitive structure while preserving the provenance
---------------------------------------------------------------------

Let us begin by downloading a gallium arsenide (GaAs) structure from the
`Crystallography Open Database <http://crystallography.net/cod/>`_ and importing
it into AiiDA.

.. note::

   You can view the structure `online <http://crystallography.net/cod/9008845.html>`_.


.. code:: bash

    wget http://crystallography.net/cod/9008845.cif
    verdi data structure import ase 9008845.cif

As before, you will get the ``PK`` of the imported structure.
We note that a ``StructureData`` can also be exported to file to various formats.
As an example, let's export the structure in XSF format and visualize it
with XCrySDen:
   
.. code:: bash

   verdi data structure export --format=xsf <PK> > exported.xsf
   xcrysden --xsf exported.xsf

You should see the GaAs supercell (8 atoms) that we downloaded 
from the COD database (in CIF format), imported into AiiDA and exported back
into a different format (XSF).

In particular, the structure that we imported (and converted from CIF
to an explicit list of atoms) used the conventional cell with 8 atoms,
rather than the primitive one (with 2 atoms only).

Getting the primitive structure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We will now use `seekpath`_ (that internally uses `spglib`_), 
to obtain the primitive cell from the conventional one.
Actually, seekpath does more: it will also standardise the orientation of
the structure, and suggest the path for a band-structure calculation.

We will not use seekpath directly, but a wrapper for AiiDA, that converts
to and from AiiDA data types automatically (in particular, it reads
directly AiiDA data nodes, and returns AiiDA nodes). The full documentation 
of these wrapper methods can be found `on this page <https://aiida.readthedocs.io/projects/aiida-core/en/latest/datatypes/kpoints.html#automatic-computation-of-k-point-paths>`_.

As a first thing, in the terminal, open an ipython shell with the AiiDA
environment pre-loaded. This can be achieved by running:

.. code:: bash
  
   verdi shell

.. note:: If you prefer working in jupyter, you can do so. 

   Open your browser (the one with jupyter that you opened in the :ref:`setup <setup jupyter oxford 2020>`
   chapter of this tutorial), then create a new Python 3 notebook (with the button "New"
   in the top right of the jupyter page, and then select "Python 3").
   
   Give the notebook a name: click on the word "Untitled" at the top, then
   type a file name (e.g. "create_supercell") and confirm.

   The only additional thing you need to do is to load the AiiDA environment.
   In the first code cell, type ``%aiida`` and confirm with Shift+ENTER.

   You should get a confirmation message "Loaded AiiDA DB environment".
   You can then work as usual in jupyter, adding the code in the following cells.

Now, in this ipython shell (or in jupyter), you can import the wrapper function (that internally uses
seekpath) as:

.. code:: python
   
   from aiida.tools import get_kpoints_path

We now want to use it. As you can see in the `documentation <https://aiida.readthedocs.io/projects/aiida-core/en/latest/apidoc/aiida.tools.data.array.kpoints.html#aiida.tools.data.array.kpoints.get_kpoints_path>`_, you need to pass
as a parameter a ``StructureData`` node (in our case, the node that you imported earlier from COD).
To load a node in the ipython shell, use the following command:

.. code:: python
   
   structure = load_node(<PK>)

where ``<PK>`` is the of the ``StructureData`` node you imported earlier.
At this point you are ready to get the primitive structure:

.. code:: python
   
   seekpath_data = get_kpoints_path(structure)
   primitive = seekpath_data['primitive_structure']

**Exercise**: Check that the ``primitive`` object is an AiiDA ``StructureData`` node, and that it is still 
not stored in the database (you can just print it). Moreover, check that you indeed obtained a
primitive structure by inspecting the unit cell using
``print(primitive.cell)``, and the list and position of the atoms with ``print(primitive.sites)``.


Preserving the provenance
~~~~~~~~~~~~~~~~~~~~~~~~~

AiiDA is focused on making it easy to track the provenance of your calculation, i.e., the history of how it
has been generated, by which calculation, and with which inputs.
If you were just to store the ``primitive`` ``StructureData`` node, you would lose its provenance.
Instead, AiiDA provides simple tools to store it automatically in the form of a graph, where nodes are either
data nodes (as the one we have just seen), or calculations (i.e., "black boxes" that get data as input, 
and create new data as output). Links between nodes represent the logical relationship between calculations and
their inputs and outputs.

While we refer to the full `AiiDA documentation`_ for more in-depth explanations, here we show the simplest way to 
run a python function while keeping the provenance at the same time.

This can be achieved by using a ``calcfunction``: this is a wrapper around python functions
(technically, a python function decorator) that takes care of storing the execution of that function in the graph.
To use it, you need first to create a simple function that gets one or more AiiDA nodes, and returns one AiiDA node
(or a dictionary of AiiDA nodes). Moreover, you need to decorate it as a ``calcfunction``, so that when it will be run,
it will be stored in the database.

Here is the complete code:

.. code:: python
   
   from aiida.engine import calcfunction

   @calcfunction
   def get_primitive(input_structure):
       from aiida.tools import get_kpoints_path
       seekpath_data = get_kpoints_path(input_structure)
       return {
           'primitive_structure': seekpath_data['primitive_structure'],
           'seekpath_parameters': seekpath_data['parameters']
       }

Once you have defined the function, run it on the ``structure`` node you loaded earlier:

.. code:: python
   
   results = get_primitive(structure)
   primitive = results['primitive_structure']

The first thing you can notice (by printing ``primitive``) is that now this node
has been automatically stored.
Additionally, you can check who created it simply as ``creator_function = primitive.creator``.
You can for instance check the name of the function that was run, using ``creator_function.attributes['function_name']``
(this returns ``get_primitive``, the name of the function that we decorated as a ``calc_function``).
Moreover, you can check the inputs of this function.

**Exercise**: Use ``creator_function.inputs.input_structure`` to get the input of the function called ``input_structure``
(the name is taken from the parameter name in the definition of the ``get_primitive`` function) and check that it
is the exact same node that you started from.

**Exercise**: Go in a bash shell (e.g., open a new terminal -- remember to also enter the virtual environment using ``workon aiida``!). You can inspect graphically the full provenance of a given node using

.. code:: bash

   verdi node graph generate <PK>

where we suggest here to use the PK of the ``creator_function``. The code will generate a PDF that you can
open, and that should look like the following image:

.. figure:: include/images/calcfunction_provenance.png
   :width: 100%

   Provenance graph for the calcfunction used to obtain the primitive structure of GaAs.

.. note:: **TAKE HOME MESSAGE**

   AiiDA makes it very easy to convert python functions into ``calcfunctions`` that, every time
   they are executed, represent their execution in the AiiDA graph.
   
   The calc function itself is represented as a Calculation Node; all its function inputs
   and its (labeled) function outputs are also stored as AiiDA data nodes and are linked
   via INPUT and CREATE links, respectively.

   It is possible to browse such graph, that tracks the *provenance* of the output data.
   Moreover, having the exact inputs tracked makes each calculation *reproducible*.

   Finally (as we have already seen as an example in the previous sections for
   calculation jobs), outputs of a calculation can become inputs to a new calculation.
   Therefore, the AiiDA data provenance graph is a **directed acyclic graph**.

.. note:: While you can run the ``get_kpoints_path`` function as many times you want (and it will return
   unstored nodes, so it will not clutter your AiiDA database), remember that *every time* you run the
   ``get_primitive()`` calc function, you will get a bunch of new nodes in the database automatically stored for you.
   

.. _spglib: https://atztogo.github.io/spglib/
.. _seekpath: https://github.com/giovannipizzi/seekpath
.. _AiiDA documentation: https://aiida.readthedocs.io/projects/aiida-core/en/v1.1.1/reference/index.html
