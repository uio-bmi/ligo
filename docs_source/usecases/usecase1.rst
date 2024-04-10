Manuscript use case 1: Out-of-distribution receptor-level simulation using LIgO
============================================================

The composition of train and test data can impact the quality and accuracy of AIRR-ML models. In our use case, we showed how splitting the train and test data may decrease predictive performance in out-of-distribution cases. With LIgO, we simulated a scenario where an immune signal is defined as one motif, but each individual carries a slightly different modification of this motif. 

We trained and evaluated a logistic regression model (LR) for receptor-level classification using two different train-test strategies. The first strategy involved a random split of all AIRs from all individuals into train and test sets, while the second strategy used a leave-one-individual-out approach, placing all AIRs from one individual into the test set and AIRs from the other individuals into the training set. Our findings revealed that LR trained on the random train-test strategy achieved higher balanced accuracy compared to LR trained on the leave-one-individual-out approach. 

In this tutorial, we give an example of a simulation configuration for a single dataset, along with detailed explanations of the parameters in the comments as needed. A detailed description of use case 1 can be found in the LIgO manuscript.

Simulation configuration
------------------------

In this use case, we considered the immune signal as a motif AA-A with four variations — AAAA, AANA, AACA, and AAGA reflecting AIRs from four different individuals. 

Specifically, the configuration below describes the simulation of a dataset consisting of:

- AIRR1: 5000 IGHs containing AAAA + 5000 IGHs without any of the four signal 4-mers;

- AIRR2: 5000 IGHs containing AACA + 5000 IGHs without any of the four signal 4-mers;

- AIRR3: 5000 IGHs containing AAGA + 5000 IGHs without any of the four signal 4-mers;

- AIRR4: 5000 IGHs containing AANA + 5000 IGHs without any of the four signal 4-mers.

.. image:: ../_static/figures/usecase1_signals.png
  :width: 500

.. code-block:: yaml

  definitions:
  motifs:
    motif1:
      seed: AAAA
    motif2:
      seed: AACA
    motif3:
      seed: AAGA
    motif4:
      seed: AANA
  signals:
    signal1:
      motifs:
      - motif1
    signal2:
      motifs:
      - motif2
    signal3:
      motifs:
      - motif3
    signal4:
      motifs:
      - motif4
  simulations:
    sim1:
      is_repertoire: true
      paired: false
      sequence_type: amino_acid
      simulation_strategy: Implanting # use implanting for simulation signal-specific AIRs
      remove_seqs_with_signals: true # remove all 4 signals from the background receptors
      keep_p_gen_dist: false
      sim_items:
        airr1: # repertoire for individual 1
          generative_model:
            default_model_name: humanIGH
            model_path: null
            type: OLGA
          is_noise: false
          number_of_examples: 1 # for demonstration purposes we simulate airr1 1 time
          receptors_in_repertoire_count: 10000 # each AIRR containing 10000 receptors
          signals:
            signal1: 0.5 # 50% of receptors (5000) should contain signal1 (AAAA)
        airr2: # repertoire for individual 2
          generative_model:
            default_model_name: humanIGH
            model_path: null
            type: OLGA
          is_noise: false
          number_of_examples: 1 # for demonstration purposes we simulate airr2 1 time
          receptors_in_repertoire_count: 10000 # each AIRR containing 10000 receptors
          signals:
            signal2: 0.5 # 50% of receptors (5000) should contain signal2 (AACA)
        airr3: # repertoire for individual 3
          generative_model:
            default_model_name: humanIGH
            model_path: null
            type: OLGA
          is_noise: false
          number_of_examples: 1 # for demonstration purposes we simulate airr3 1 time
          receptors_in_repertoire_count: 10000 # each AIRR containing 10000 receptors
          signals:
            signal3: 0.5 # 50% of receptors (5000) should contain signal3 (AAGA)
        airr4: # repertoire for individual 4
          generative_model:
            default_model_name: humanIGH
            model_path: null
            type: OLGA
          is_noise: false
          number_of_examples: 1 # for demonstration purposes we simulate airr4 1 time
          receptors_in_repertoire_count: 10000 # each AIRR containing 10000 receptors
          signals:
            signal4: 0.5 # 50% of receptors (5000) should contain signal4 (AANA)
instructions:
  inst1:
    export_p_gens: false # we don't need pgens for this use case
    max_iterations: 10000
    number_of_processes: 32
    sequence_batch_size: 100000
    simulation: sim1
    type: LigoSim
output:
  format: HTML
  
  

ML configuration
-----------------

.. image:: ../_static/figures/usecase1_splits.png
  :width: 800
