Installing LIgO
===================

.. toctree::
   :maxdepth: 2

There are two options for installing LIgO:

#. Install on the local machine either from PyPI or from GitHub
#. Use Docker image

Installing LIgO on the local machine
---------------------------------

.. note::

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

4. To be able to export full-length sequences, it is necessary to also download the reference data using Stitchr:

.. code-block:: console

  stitchrdl -s human

For more information on downloading data using Stitchr, see `Stitcher documentation <https://jamieheather.github.io/stitchr/installation.html>`_.


Use LIgO with Docker
----------------------

.. note::

   This tutorial assumes you have Docker installed on your machine. To install it, see `the official Docker documentation <https://docs.docker.com/get-docker/>`_.

Getting started with LIgO and Docker
********************************************

Once you have Docker working on your machine, put the following content in the specs.yaml in the current working directory:

.. indent with spaces
.. code-block:: yaml

 definitions:
motifs:
  motif1:
    seed: AS
  motif2:
    seed: G/G
    max_gap: 2
    min_gap: 1
signals:
  signal1:
    v_call: TRBV7
    motifs: [motif1]
  signal2:
    motifs: [motif2]
simulations:
  sim1:
    is_repertoire: false
    paired: false
    sequence_type: amino_acid
    simulation_strategy: RejectionSampling
    remove_seqs_with_signals: true # remove signal-specific AIRs from the background
    sim_items:
      sim_item1: # group of AIRs with the same parameters
        generative_model:
          chain: beta
          default_model_name: humanTRB
          model_path: null
          type: OLGA
        number_of_examples: 100
        signals:
          signal1: 1
      sim_item2:
        generative_model:
          chain: beta
          default_model_name: humanTRB
          model_path: null
          type: OLGA
        number_of_examples: 100
        signals:
          signal2: 1
      sim_item3:
        generative_model:
          chain: beta
          default_model_name: humanTRB
          model_path: null
          type: OLGA
        number_of_examples: 100
        signals: {} # no signal
instructions:
  my_sim_inst:
    export_p_gens: false
    max_iterations: 100
    number_of_processes: 4
    sequence_batch_size: 1000
    simulation: sim1
    type: LigoSim


Then, use the following command to download and run the Docker image with LIgO analysis. This will do the following:

1. create the Docker container with the given name (here: :code:`my_container`),

2. bind the current working directory to the path /data inside the container which will make the data from the working directory visible inside the container and which will keep the data placed there visible after the container is stopped,

3. run an LIgO analysis using specs.yaml from the current folder and store the output in the new 'output' directory in the current working directory:

.. code-block:: console

  docker run -it -v $(pwd):/data --name my_container milenapavlovic/ligo ligo /data/specs.yaml /data/output/

This analysis will simulate 300 TCR beta receptors and store the results in the `/data/output` folder.

To exit the Docker container, use the following command:

.. code-block:: console

  exit

Using the Docker container for longer LIgO runs
***************************************************

If you expect the analysis to take more time, you can start the container as a background process. The command to run in that case would be the following:

.. code-block:: console

  docker run -itd -v $(pwd):/data --name my_container milenapavlovic/ligo ligo /data/specs.yaml /data/output/

To see the logs, run the following command with the container name (here: :code:`my_container`):

.. code-block:: console

  docker logs my_container

To see the list of available containers, you can use the following command:

.. code-block:: console

  docker ps -a

If you just started the container with the previous command, the output showing the list of available containers should look similar to this:

.. code-block:: console

  CONTAINER ID        IMAGE                     COMMAND             CREATED             STATUS              PORTS               NAMES
  e799e644e479        milenapavlovic/ligo   "/bin/bash"         34 seconds ago      Up 33 seconds                           my_container

To stop the container, run the following command where the argument is the name of your container:

.. code-block:: console

  docker stop my_container

To delete the container, run the following command where the argument is the name of your container:

.. code-block:: console

  docker rm my_container
