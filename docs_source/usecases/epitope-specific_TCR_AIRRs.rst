Simulating epitope-specific TCRs and validating their properties 
===================

During the development of a new epitope-TCR prediction method, it might be useful to simulate training data to test it or study potential biases in model performance. In this tutorial, we simulate epitope-specific TCR data, i.e., a collection of TCRs derived from different individuals that are all recognizing the same epitope. Note that LIgO-simulated DATA can only resemble the general structure of epitope-specific TCRs. The actual specificities of these TCRs cannot be simulated, and thus the final simulated data are not guaranteed to contain only TCRs recognizing the same epitope. Otherwise, the problem of predicting epitope-TCR binding would be solved, and no models should be trained anymore.
 
In this tutorial, one epitope-specific TCR beta receptors are simulated from three user-defined motifs, which are considered to describe the subsequences within TCRs that are epitope-specific. Next, we ensure that the simulated data is biologically relevant by comparing the simulated TCRs to the experimental epitope-specific data.  


Simulating of the epitope-specific TCRs
-------------------------

We defined an epitope-specific motif using the VDJdb dtabase. Further details on transforming known epitope-specific TCRs from VDJdb into LIgO motifs can be found in the tutorial :ref:`Constructing LIgO motifs inspired by VDJdb`. In this simulation, we will utilize long seeds created in the same tutorial :ref:`Constructing LIgO motifs inspired by VDJdb`. The rejection sampling method was used to avoid introducing additional artifacts to LIgO-simulated TCRs. 

The yaml file below describes simulation parameters used for LIgO simulation. You can find more details on how the parameters for the simulation were chosen in the tutorial :ref:`Constructing LIgO motifs inspired by VDJdb` and find more information about how to run receptor-level simulation using the quickstart :ref:`How to use LIgO for receptor-level simulation`.
  
.. code-block:: yaml

  definitions:
    motifs: # define motifs based on long seeds
      motif1:
        hamming_distance_probabilities:
          0: 0.1
          1: 0.2
          2: 0.7
        seed: ELSGINQP
      motif2:
        hamming_distance_probabilities:
          0: 0.1
          1: 0.2
          2: 0.7
        seed: SPAGGTYE 
      motif3:
        hamming_distance_probabilities:
          0: 0.1
          1: 0.2
          2: 0.7
        seed: SGGDVREE 
    signals:
      signal1:
        motifs:
        - motif1
        sequence_position_weights:
          '104': 0 # we did not want to start the motif at the first position, i.e. IMGT position 104
      signal2:
        motifs:
        - motif2
        sequence_position_weights:
          '104': 0 # we did not want to start the motif at the first position, i.e. IMGT position 104
      signal3:
        motifs:
        - motif3
        sequence_position_weights:
          '104': 0 # we did not want to start the motif at the first position, i.e. IMGT position 104
    simulations:
      sim1:
        is_repertoire: false
        paired: false
        sequence_type: amino_acid
        simulation_strategy: RejectionSampling
        sim_items:
          var1:
            generative_model:
              default_model_name: humanTRB
              type: OLGA
            is_noise: false
            number_of_examples: 300 # simulate 300 TCRs 
            signals: 
              signal1: 1 # all TCRs having signal1
          var2:
            generative_model:
              default_model_name: humanTRB
              type: OLGA
            is_noise: false
            number_of_examples: 300 # simulate 300 TCRs 
            signals:
              signal2: 1 # all TCRs having signal2
          var3:
            generative_model:
              default_model_name: humanTRB
              type: OLGA
            is_noise: false
            number_of_examples: 300 # simulate 300 TCRs 
            signals:
              signal3: 1 # all TCRs having signal3
  instructions:
    inst1:
      export_p_gens: false
      max_iterations: 2000
      number_of_processes: 8
      sequence_batch_size: 10000
      simulation: sim1
      type: LigoSim
  output:
    format: HTML


Step 4: Setting the instructions
----------------------

After defining the simulation, you can update the instructions to execute this simulation. Important factors are the number of TCR sequences LIgO has to generate in every iteration (sequence_batch_size) and the maximum number of iterations (max_iterations).

.. code-block:: yaml

  instructions:
   inst1:
     export_p_gens: true
     max_iterations: 2000
     number_of_processes: 8
     sequence_batch_size: 10000
     simulation: sim1
     type: LigoSim

When achieving the number of required TCRs before the maximum number of iterations, the LIgO simulation will stop. However, when the number of required TCRs is not reached after the maximum number of iterations, the following error will be reported:

*LigoSimInstruction: maximum iterations were reached, but the simulation could not finish with parameters:…*

In this situation, you have multiple options to proceed. First of all, take a look at the results and see how many TCRs were generated. In case of an error, the results for every simulation item are stored in
  
.. code-block:: yaml
  
  results/inst1/simulation_item/processed_sequences/name_of_the_signal.tsv

For this tutorial, the following files should be consulted in case of a LigoSimInstruction error

.. code-block:: yaml

  results/inst1/var1/processed_sequences/signal1.tsv.
  results/inst1/var2/processed_sequences/signal2.tsv.
  results/inst1/var3/processed_sequences/signal3.tsv.

How to handle the maximum iterations were reached error?

#. If you only need a few more TCRs, you can increase the sequence_batch_size and the max_iterations and wait a bit longer.  If no additional data is needed, you could already work with the data that has been generated.

#. In case the number of generated TCRs is very low, you must adapt your motifs to allow more variation, i.e. shorten the seed, increase the hamming distance or start with a new seed.

**Tip**: Before initiating a large simulation process, first estimate the success of the simulation by running the simulation feasibility report. For more details see :ref:`How to check feasibility of the simulation parameters`


Step 5: Run your simulation
-----------------------------

After setting all options in the YAML file, you can start your simulation by specifying the required YAML file and the name of the results folder that will be created.

.. code-blocks:: yaml

ligo specs.yaml results


Additional step: Inspect your simulated repertoire
------------------------------
