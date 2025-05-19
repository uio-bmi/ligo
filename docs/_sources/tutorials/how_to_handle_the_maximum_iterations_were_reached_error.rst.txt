How to handle the maximum iterations were reached error
----------------------

LIgO has two parameters, which may impact succuss of the simulation: the number of AIRs LIgO has to generate in every iteration (sequence_batch_size) and the maximum number of iterations (max_iterations).

When achieving the number of required AIRs before the maximum number of iterations, the LIgO simulation will stop. However, when the number of required AIRs is not reached after the maximum number of iterations, the following error will be reported:

*LigoSimInstruction: maximum iterations were reached, but the simulation could not finish with parameters:…*

In this situation, you have multiple options to proceed. First of all, take a look at the results and see how many AIRs were generated. In case of an error, the results for every simulation item are stored in
  
.. code-block:: yaml
  
  results/inst1/simulation_item/processed_sequences/name_of_the_signal.tsv

For example, if the name of your simulated signal is "signal1" then the signal-specific AIRs will be stored in this file:

.. code-block:: yaml

  results/inst1/var1/processed_sequences/signal1.tsv

Tips for handling the maximum iterations were reached error
=====================================

#. If you only need a few more AIRs, you can increase the sequence_batch_size and the max_iterations and wait a bit longer. If no additional data is needed, you could already work with the data that has been generated.

#. In case the number of generated AIRs is very low, you must adapt your signal definition or change your simulation method from rejection sampling to signal implantation.

.. note::

   Before initiating a large simulation process, first estimate the success of the simulation by running the simulation feasibility report. For more details see :ref:`How to check feasibility of the simulation parameters`
