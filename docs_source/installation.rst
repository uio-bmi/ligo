Installing LIgO
===================

.. toctree::
   :maxdepth: 2

There are two options for installing LIgO:

#. Install on the local machine either from PyPI or from GitHub
#. Use Docker image

Installing LIgO on the local machine
---------------------------------

Requirements: Python 3.11 or later

To install LIgO on the local machine with pip:

1. Make a virtual environment where LIgO will be installed to avoid package versioning issues or collisions with the packages installed for other projects:

.. code-block:: console

  python -m venv ligo_env

2. Activate virtual environment:

.. code-block:: console

  source ligo_env/bin/activate

3. Install LIgO from PyPI (recommended):

.. code-block:: console

  pip install ligo

Alternatively, to install LIgO from GitHub run the following:

.. code-block:: console

  pip install git+https://github.com/uio-bmi/ligo.git


Use LIgO with Docker
----------------------

More information on using LIgO with Docker is coming soon!
