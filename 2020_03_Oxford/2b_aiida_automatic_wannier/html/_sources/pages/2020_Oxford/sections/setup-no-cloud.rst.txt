Getting set up
==============

Download the correct Quantum Mobile version listed 
:ref:`in the homepage of this event<Oxford 2020 Homepage>`.

.. note:: The credentials of the Quantum Mobile VM that you can download
   from the main page of this tutorial material
   are the following: username: ``max``, password: ``moritz``.

You can find some troubleshooting, in case you have problems, on the
`Quantum Mobile FAQ page`_.

.. _Quantum Mobile FAQ page: https://github.com/marvel-nccr/quantum-mobile/wiki/Frequently-Asked-Questions

.. _setup jupyter oxford 2020:

Start jupyter
-------------

Once connected to your virtual machine, to use AiiDA open a terminal and type 

.. code:: bash

     workon aiida

This will enable the virtual environment in which AiiDA is installed,
allowing you to use AiiDA. Now, to start a jupyter notebook (you might
need it later in the tutorial) type in the same shell:

.. code:: bash

     jupyter notebook

This will run a server with a web application called ``jupyter``, which
is used to create interactive python notebooks.
This will also open the default browser (in the VM) and allow you to use
jupyter.
Keep the browser open, so you can use jupyter later when needed.

Keep also the terminal open (just minimise the window).
If you need to use the terminal, just open another one (right click on the terminal
icon on the left bar, and choose "New terminal").

Additional useful notes
-----------------------
Read through the next sections if you are interested in knowing how to download files
into the virtual machine, how to troubleshoot typical problems, or how to get additional help.

Downloading files
~~~~~~~~~~~~~~~~~

Throughout this tutorial, you will encounter links to download python scripts, jupyter notebooks and more.
These files should be downloaded to the environment/working directory you use to run the tutorial.
In particular, when running the tutorial on a linux virtual machine, copy the link address and download the files to the machine using the ``wget`` utility on the terminal:

.. code:: bash

   wget '<LINK>'

where you replace ``<LINK>`` with the actual HTTPS link that you copied from the tutorial text in your browser.
This will download that file in your current directory.


Troubleshooting
~~~~~~~~~~~~~~~

-  If you get errors ``ImportError: No module named aiida`` or
   ``No command ’verdi’ found``, double check that you have loaded the
   virtual environment with ``workon aiida`` before launching ``python``,
   ``ipython`` or the ``jupyter`` notebook server.

Getting help
~~~~~~~~~~~~

There are a number of helpful resources available to you for getting more information about AiiDA.
Please consider:

 * consulting the extensive `AiiDA documentation <https://aiida-core.readthedocs.io/en/latest/>`_
 * opening a new issue on the `tutorial issue tracker <https://github.com/aiidateam/aiida-tutorials/issues>`_
 * asking your neighbor
 * asking a tutor.

.. Add here a link if you are creating a slack channel for the tutorial
