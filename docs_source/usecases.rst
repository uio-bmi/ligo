Use case examples
================================

This page provides examples on how LIgO can be used to validate AIRR-ML approaches. All use cases assume you have LIgO already installed. For details on how to do that, see :ref:`Installing LIgO`.


The LIgO manuscript showcases LIgO on two use cases. The following sections provide a description of how to reproduce these use cases.

1. :ref:`Manuscript use case 1: Out-of-distribution receptor-level simulation using LIgO`

2. :ref:`Manuscript use case 2: Limitations of conventional encoding schemes for repertoire-level binary classification when immune signals co-occur within the same AIR`


The following group of use cases is inspired by the manucript **"Revealing the hidden sequence distribution of epitope-specific TCR repertoires and its influence on machine learning model performance"** (`biorxiv <https://https://www.biorxiv.org/content/10.1101/2024.10.21.619364v1>`_). From these use cases you can learn how to define LIgO motifs inspired by VDJdb database, simulate epitope-specific TCRs based on these motifs, and inspect the simulated TCRs compared to experimental data.

1. :ref:`Constructing LIgO motifs inspired by a database of TCR sequences with known antigen specificities`

2. :ref:`Simulating epitope-specific TCRs and validating their properies`


List of all usecases
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
  :maxdepth: 1

  usecases/usecase1
  usecases/usecase2
  usecases/TCR_motifs.rst
  usecases/epitope-specific_TCR_AIRRs.rst


