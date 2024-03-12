How to check feasibility of the simulation parameters
-------------------------------------------------------

LIgO supports simulations that consist of any immune signal (any k-mer or PWM or any combination of them),
so it might hard to know in advance how frequent a signal is or how it works with other signals of interest. For that
purpose, LIgO provides a separate analysis called **FeasibilitySummary**. It is especially useful if rejection sampling is
used as a simulation strategy or when removing background
receptors that accidentally contain some of the signals when implanting is used as a simulation strategy.

This analysis simulates a predefined number of sequences for each generative model provided in the simulation and reports
the following information per generative model:

- frequencies of each signal,
- how many sequences contain how many signals,
- joint probabilities for pairs of signals,
- conditional probabilities of observing one signal in the sequences given that another is already observed,
- sequence length distribution,
- warnings if some signals are very rare or very frequent.

This tutorial shows how to run the **FeasibilitySummary** analysis.


Step 1: Define potential immune signals and the simulation
=======================================================================

The first step is to define a simulation. For example, in this tutorial we will define 4 signals, with one motif each.
We will request to simulate 2 immune repertoires corresponding to 2 individuals: one repertoire to have signal1 in 50% of the
sequences and signal4 in 20%. The other repertoire will be specified to have 10% of sequences with signal1 and 20% of
sequences with signal2. For more details on defining immune signals, see :ref:`How to define immune signals and immune events`.

The specification for the signals and the simulation looks like this:

.. code-block:: yaml

    motifs:
      motif1:
        seed: AS
      motif2:
        seed: G
      motif3:
        seed: C
      motif4:
        seed: SLVTY
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
        sim_items:
          repertoire_group1:
            generative_model:
              default_model_name: humanTRB
              model_path: null
              type: OLGA
            immune_events:
              ievent1: true
              ievent2: false
            is_noise: false
            number_of_examples: 1
            receptors_in_repertoire_count: 6
            seed: 100
            signals:
              signal1: 0.5
              signal4: 0.2
          repertoire_group2:
            generative_model:
              default_model_name: humanTRB
              model_path: null
              type: OLGA
            immune_events:
              ievent1: false
              ievent2: false
            is_noise: false
            number_of_examples: 1
            receptors_in_repertoire_count: 10
            seed: 2
            signals:
              signal1: 0.1
              signal2: 0.2
        simulation_strategy: RejectionSampling

Step 2: Define how to generate the summary
===================================================

For the simulation with the given parameters, we can now specify how to provide the feasibility summary. We need to provide
the number of receptor sequences to generate to conduct the analysis and connect it to the simulation we are interested in.
The higher the number of generated sequences, the better the estimate of signal occurrences. However, higher number of
sequences and their annotation and summarization will result in longer running times.

.. code-block:: yaml

    inst1:
      sequence_count: 100
      simulation: sim1
      type: FeasibilitySummary

Step 3: Run the analysis and explore results
================================================

The full specification of the feasibility summary is the following:

.. code-block:: yaml

  definitions:
    motifs:
      motif1:
        seed: AS
      motif2:
        seed: G
      motif3:
        seed: C
      motif4:
        seed: SLVTY
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
        sim_items:
          repertoire_group1:
            generative_model:
              default_model_name: humanTRB
              model_path: null
              type: OLGA
            immune_events:
              ievent1: true
              ievent2: false
            is_noise: false
            number_of_examples: 1
            receptors_in_repertoire_count: 6
            seed: 100
            signals:
              signal1: 0.5
              signal4: 0.2
          repertoire_group2:
            generative_model:
              default_model_name: humanTRB
              model_path: null
              type: OLGA
            immune_events:
              ievent1: false
              ievent2: false
            is_noise: false
            number_of_examples: 1
            receptors_in_repertoire_count: 10
            seed: 2
            signals:
              signal1: 0.1
              signal2: 0.2
        simulation_strategy: RejectionSampling
  instructions:
    inst1:
      sequence_count: 100
      simulation: sim1
      type: FeasibilitySummary
  output:
    format: HTML

Save this specification as `specs.yaml` and run the feasibility analysis:

.. code-block:: console

    ligo specs.yaml simulation_output

Under the `simulation_output` folder, open the `index.html` file to explore the results.
