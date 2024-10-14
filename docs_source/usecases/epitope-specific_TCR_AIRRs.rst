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

How to increase simulation complexity if required
----------------------

In this tutorial, we demonstrate how to simulate epitope-specific T-cell receptors using seeds obtained from the VDJdb (Shugay et al. 2018). One way to increase simulation complexity is to replace the seed-based motif with a position weight matrix (PWM) motif. To do this, one should:

1. Select a set of TCRs from VDJdb sharing the same epitope specificity. To obtain accurate PWMs, consider epitope sequences containing a sufficient number of epitope-specific TCRs.

2. Cluster the epitope-specific TCRs to obtain epitope-specific PWMs. This step can be performed using a tool like the clustcr tool. For more information on clustcr tool, see `clustcr documentation <https://svalkiers.github.io/clusTCR/>`_.

3. Use the epitope-specific PWMs to simulate epitope-specific TCRs using rejection sampling or signal implanting.




Inspecting the simulated TCRs
------------------------------
