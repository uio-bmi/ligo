Simulating epitope-specific TCR repertoires and validating their properties 
===================

  
During the development of a new epitope-TCR prediction method, it might be useful to simulate training data to test it or study potential biases in model performance. In this tutorial, the simulation of epitope-specific TCR repertoire data, where an epitope-specific TCR repertoire is a collection of TCRs derived from different individuals that are all recognizing the same epitope. Note that all simulated TCR repertoires can only resemble the general structure of epitope-specific TCR repertoires. The actual specificities of these TCRs cannot be simulated, and thus the final simulated repertoires are not guaranteed to contain only TCRs recognizing the same epitope. Otherwise, the problem of predicting epitope-TCR binding would be solved, and no models should be trained anymore.
 
In this tutorial, one epitope-specific TCR beta repertoire is simulated from three user-defined motifs, which are considered to describe the subsequences within TCRs that are epitope-specific. Next, we ensure that the simulated data is biologically relevant by comparing the simulated TCR repertoire to the experimental epitope-specific data.  

Simulating of the epitope-specific TCR repertoire
-------------------------

  
To ensure that all simulated TCR sequences are biologically relevant, the rejection sampling method is recommended (see Step 3). This method first generates a list of TCR sequences and afterwards removes all TCRs that do not contain a user-defined motif. Two options exist to describe this motif: (1) start from a seed and define all possible deviations that are allowed using gaps and hamming distances or (2) start from a PWM. In the case of generating a hypothetical epitope-specific TCR repertoire, i.e., the exact binding motif is not known, it is recommended to keep the motif as simple as possible, i.e., using only a seed and hamming distances. For simplicity, this seed can be derived from known epitope-specific TCR sequences. 

In this tutorial, three seeds were defined from three TCR beta sequences in the VDJdb, all recognizing one epitope (see the table below). To transform these TCRs into seeds, a subset of these TCRs needed to be removed. In general, the epitope-binding motif is located in the middle of CDR3 beta sequences, while the beginning and end are responsible for HLA-binding. Hence, the center of the CDR3 beta sequence is used as seed. Arbitrary the three first and three last amino acids are removed from the TCR sequences to derive a seed.

.. list-table:: Transforming known epitope-specific TCRs into seeds
   :header-rows: 1

   * - TCR beta sequence
     - TRBV gene
     - TRBJ gene
     - Epitope
     - Seed 
   * - CSVELSGINQPQHF
     - TRBV29-1
     - TRBJ1-5
     - GTSGSPIINR
     - ELSGINQP
   * - CASSPAGGTYEQYF
     - TRBV11-2
     - TRBJ2-7
     - GTSGSPIINR
     - SPAGGTYE
   * - CASSGGDVREEQYF
     - TRBV9
     - TRBJ2-7
     - GTSGSPIINR
     - SGGDVREE

After describing the seeds, you can list all possible deviations that are allowed from these seeds. The simplest method is to make use of a set of hamming distances:

.. code-block:: yaml

  motifs:
   motif1:
     alphabet_weights: null
     hamming_distance_probabilities:
       0: 0.1
       1: 0.2
       2: 0.7
     position_weights: null
     seed: ELSGINQP
   motif2:
     alphabet_weights: null
     hamming_distance_probabilities:
       0: 0.1
       1: 0.2
       2: 0.7
     position_weights: null
     seed: SPAGGTYE
   motif3:
     alphabet_weights: null
     hamming_distance_probabilities:
       0: 0.1
       1: 0.2
       2: 0.7
     position_weights: null
     seed: SGGDVREE

The first number describes the Hamming distance, the second number is the probability of the final motif having this Hamming distance. The latter is only relevant for implanting. However, all values should sum up to 1. To select the maximum hamming distance, consider the length of your seed and the aimed diversity of the final TCR repertoire. Shorter seeds require lower Hamming distances. However, if one only wishes to simulated TCRs looking very similar to the seed, one can also lower the hamming distance. Here, a maximum hamming distance of two was selected so that the diversity of the simulated epitope-specific TCR repertoire does not become too large.

.. note::

**Tip**: In case you do not derive your seeds from known TCR sequences, make sure your seeds are not too short. Seeds with only a few amino acids will give rise to TCR repertoires where the repertoire motifs do not overlap with the seeds. See tutorial :ref:`How to define immune signals and immune events`


Step 2: Define the signals
--------------------------


A signal is defined by one or more motifs, the location of these motifs (optional) and the V/J genes (optional). In this tutorial, every motif from step 1 is used to generate one signal. If you want to simulate a repertoire with three motifs, you must define three signals. Defining a signal with a motif is done by adding the name of the motif (e.g. ‘motif1’) underneath the signal name (e.g. ‘signal1’).
 
In addition, you can decide on the position of the motif within the simulated TCR sequences using the sequence_position_weights option. In this example, the exact location of the motif was not important. However, we did not want to start the motif at the first position, i.e. IMGT position 104, since the first amino acid of every CDR3 beta sequence is the conserved Cysteine. Hence, the weight at this position was set to 0 for every signal.
 
In case you aim to enforce the V/J genes of the signal, this can be done using the v_call and j_call parameters. However, after simulating both repertoires with and without predefined genes, it was clear that the latter resembled true repertoires better. Hence, no V/J genes are defined in this tutorial.

.. code-block:: yaml

  signals:
     signal1:
       motifs:
       - motif1
       sequence_position_weights:
         '104': 0
     signal2:
       motifs:
       - motif2
       sequence_position_weights:
         '104': 0
     signal3:
       motifs:
       - motif3
       sequence_position_weights:
         '104': 0

Step 3: Define the simulation
---------------------------------

During the simulation, the generated TCRs are compared with the signals that were defined in step 2. To report the exact signal for every TCR, one simulation item needs to be generated for each signal. In this example, the simulation items are called ‘var1’, ‘var2’ and ‘var3’. The RejectionSampling method is used to make sure that all sequences are biologically relevant.

For every simulation item, you can choose how many TCRs you want to retain. Since TCRs with a higher generation probability will have more chances of being selected, we chose to generate a large set of TCRs for each individual signal. This will increase the chances of also selecting TCRs with a lower probability in the final repertoire.

.. code-block:: yaml

  simulations:
    sim1:
      is_repertoire: false
      paired: false
      sequence_type: amino_acid
      simulation_strategy: RejectionSampling
      sim_items:
        var1:
          generative_model:
            chain: beta
            default_model_name: humanTRB
            model_path: null
            type: OLGA
          immune_events: {}
          is_noise: false
          number_of_examples: 300
          receptors_in_repertoire_count: null
          signals: 
            signal1: 1
        var2:
          generative_model:
            chain: beta
            default_model_name: humanTRB
            model_path: null
            type: OLGA
          immune_events: {}
          is_noise: false
          number_of_examples: 300
          receptors_in_repertoire_count: null
          signals:
            signal2: 1
        var3:
          generative_model:
            chain: beta
            default_model_name: humanTRB
            model_path: null
            type: OLGA
          immune_events: {}
          is_noise: false
          number_of_examples: 300
          receptors_in_repertoire_count: null
          signals:
            signal3: 1


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
