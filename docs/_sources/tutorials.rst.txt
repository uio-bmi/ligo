Tutorials
==========

This page provides an overview of tutorials to get started with LIgO. All tutorials assume you have LIgO already installed.
For details on how to do that, see :ref:`Installing LIgO`.

Each LIgO simulation begins with defining immune signals and immune events. To learn how to construct immune signals and events in the YAML specification file, see this tutorial:

- :ref:`How to define immune signals and immune events`


When immune events and immune signals are defined, the user should choose between two simulation strategies — rejection sampling or signal implantation. Also we recommend users to assess feasibility of defined simulation parameters before running the main simulation. See the tutorials below:

- :ref:`How to choose between rejection sampling and signal implantation`

- :ref:`How to check feasibility of the simulation parameters`

- :ref:`How to handle the maximum iterations were reached error`


These tutorials cover the more complex usage of LIgO simulations. For basic usage of LIgO simulation see :ref:`Quickstart` tutorials.

- :ref:`How to simulate co-occuring immune signals`

- :ref:`Paired chain simulations in LIgO`

- :ref:`Simulation with custom signal functions`

The following tutorials are inspired by the manucript **"Revealing the hidden sequence distribution of epitope-specific TCR repertoires and its influence on machine learning model performance"** by Gielis et al (`biorxiv <https://www.biorxiv.org/content/10.1101/2024.10.21.619364v1>`_). From these tutorials you can learn how to define LIgO motifs inspired by VDJdb database, simulate epitope-specific TCRs based on these motifs, and inspect the simulated TCRs compared to experimental data.

1. :ref:`Constructing LIgO motifs inspired by a database of TCR sequences with known antigen specificities`

2. :ref:`Simulating epitope-specific TCRs and validating their properties`


List of all tutorials
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
  :maxdepth: 1

  tutorials/how_to_define_immune_signals_and_events
  tutorials/how_to_choose_simulation_strategy
  tutorials/how_to_check_feasibility_of_sim_params
  tutorials/how_to_handle_the_maximum_iterations_were_reached_error
  tutorials/simulation_with_custom_signal_functions
  tutorials/how_to_simulate_paired_chain_data
  tutorials/how_to_simulate_co-occuring_signals
  tutorials/TCR_motifs.rst
  tutorials/epitope-specific_TCR_AIRRs.rst
