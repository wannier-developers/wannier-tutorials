.. _Oxford 2020 Homepage:

2020 Wannier tutorial "Virtual Edition"
=======================================

+-----------------+----------------------------------------------------------------------------------------------------------------------+
| Related resources                                                                                                                      |
+=================+======================================================================================================================+
| Virtual Machine | `Quantum Mobile 20.03.1`_                                                                                            |
+-----------------+----------------------------------------------------------------------------------------------------------------------+
| python packages | `aiida-core 1.1.0`_, `aiida-quantumespresso 3.0.0a6`_ , `aiida-wannier90 2.0.0`_, `aiida-wannier90-workflows 1.0.1`_ |
+-----------------+----------------------------------------------------------------------------------------------------------------------+
| codes           | `Quantum Espresso 6.5`_, `Wannier90 3.1.0`_                                                                          |
+-----------------+----------------------------------------------------------------------------------------------------------------------+

.. _Quantum Mobile 20.03.1: https://github.com/marvel-nccr/quantum-mobile/releases/tag/20.03.1
.. _aiida-core 1.1.0: https://pypi.org/project/aiida-core/1.1.0
.. _aiida-quantumespresso 3.0.0a6: https://github.com/aiidateam/aiida-quantumespresso/releases/tag/v3.0.0a6
.. _aiida-wannier90 2.0.0: https://github.com/aiidateam/aiida-wannier90/releases/tag/v2.0.0
.. _Quantum Espresso 6.5: https://github.com/QEF/q-e/releases/tag/qe-6.5
.. _Wannier90 3.1.0: https://github.com/wannier-developers/wannier90/releases/tag/v3.1.0
.. _aiida-wannier90-workflows 1.0.1: https://github.com/aiidateam/aiida-wannier90-workflows/releases/tag/v1.0.1
.. _Custom VM used for the Oxford 2020 tutorial: https://object.cscs.UPDATEME

.. note:: The credentials of the Quantum Mobile VM are the following: username: ``max``, password: ``moritz``.
   Also, when you start the VM, to make it more performant you might want to set 2 CPUs, and 2GB of RAM or more.
   If the machine becomes slow after a few hours of use, in VirtualBox 6 you can change the settings of the
   graphics controller to VMSVGA.

These are the hands-on materials from the 1-day AiiDA tutorial, part of the 
`Wannier90 v3.0: new features and applications  <http://www.wannier.org/events/school-2020-virtual-edition/>`_,
that should have been held on March 25-27, 2020 in Oxford (UK) but was converted to a "Virtual Edition"
(as discussed on the online page).


AiiDA-Wannier90 hands-on 
^^^^^^^^^^^^^^^^^^^^^^^^

Demo
----

.. toctree::
   :maxdepth: 6
   :numbered:

   ./sections/setup-no-cloud
   ./sections/first_taste
   ./sections/automated_wannierisation
   
In-depth tutorial
-----------------
In this tutorial, no in-depth tutorial on AiiDA has been presented.

If you are interested, you can check the in-depth tutorial of the :ref:`Xiamen 2019 tutorial <Xiamen 2019 Homepage>`
or of the :ref:`EPFL 2019 tutorial <EPFL 2019 Homepage>`.



