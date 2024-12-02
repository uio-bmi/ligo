Quickstart
==========

How to run LIgO
---------------------------------

You can run LIgO in the command line using the following command:

.. code-block:: console

  ligo specs.yaml output_folder

Where

* **specs.yaml** — simulation parameters described by the user in a yaml file. Please see :doc:`specification` for more information about LIgO parameters.
* **output_folder** — output folder name defined by the user (should not exist before the run). 

How to explore LIgO results
---------------------------------

The output folder structure is the same for all LIgO runs. The output folder should include:

- **index.html**: main output file which gives an overview of the simulation: link to the full specification, the used LIgO version, some general information on the dataset and the link to the dataset exported in the standard AIRR format
- **full_specs.yaml** file: includes the specification and default parameters if any of the parameters were left unfilled
- **inst1** folder: this folder name is the same as the name given to the instruction by the user; all results are located here; the simulated dataset is located under `inst1/exported_dataset/airr/`
- **HTML_output** folder: presentation of figures and reports if specified


Quickstart tutorials
---------------------------------


.. toctree::
  :maxdepth: 1

  quickstart/receptor_level_simulation
  quickstart/repertoire_level_simulation
  quickstart/overview_of_ligo_parameters
