How to define immune signals and immune events
-------------------------------------------------

Adaptive immune receptors (AIRs) specifically recognize various antigens, so they can be labeled with antigen specificity.
Adaptive immune receptor repertoires (AIRRs) coming from individual patients can in a similar way be labeled with individual's disease state(s).
To facilitate development and benchmarking of AIRR-related machine learning models, we focus on biological **immune events** (e.g., disease, allergy, vaccination)
and **immune signals** that reflect the binding rules to the immune event antigens. Because of this formalization,
multiple immune signals can be associated with a single immune event.

In this tutorial, we describe this formalization we make in more details and connect it to the simulation specification.
More details on each of the options in the specification can be found under :ref:`YAML specification` page.

To define an immune signal on the AIR level, we define the following:

- a set of **motifs** determining the content of the receptor sequence, where motifs are defined as a distribution over amino acids or nucleotides,
- motif locations in the CDR3,
- V gene,
- J gene.

Motifs
========

LIgO allows for two types of motifs:

- a motif based on the seed string with possible gaps and allowed variations from the seed and
- a positional weight matrix describing multinomial distribution of amino acids or nucleotides over the motif positions.

Seed motif
*************

Here is an example of the motif definition based on a seed. It is possible to define seed that can optionally contain a
gap denoted with `/` sign, minimum and maximum size of the gap, probabilities of different Hamming distances (how many
letters in the motif can be changed and with what probability), position weights (probabilities that a letter in the
seed will be changed for each letter), and alphabet weights (which letters to pick for replacement to implement the
required Hamming distance).

.. code-block:: yaml

  my_simple_motif: # the name of the motif used for reference later
        seed: AAA # motif is always AAA
  my_gapped_motif: # the name of the more complex motif where / sign denotes a possible gap location
        seed: AA/A # this motif can be AAA, AA_A, CAA, CA_A, DAA, DA_A, EAA, EA_A
        min_gap: 0 # how many gaps can there be: min 0 and max 1
        max_gap: 1
        hamming_distance_probabilities: # it can have a max of 1 substitution
            0: 0.7
            1: 0.3
        position_weights: # note that index 2, the position of the gap, is excluded from position_weights
            0: 1 # only first position can be changed
            1: 0
            3: 0
        alphabet_weights: # the first A can be replaced by C, D or E
            C: 0.4
            D: 0.4
            E: 0.2


Positional weight matrix
***************************

Motifs can alternatively be defined as positional weight matrices (PWMs). For importing PWMs (and later annotation of
sequences with motifs defined as PWMs), LIgO relies on bionumpy library and supports the formats supported by the library.
For more information, see `bionumpy documentation on PWMs <https://bionumpy.github.io/bionumpy/tutorials/position_weight_matrix.html>`_.

Here is an example of a motif defined in the `JASPAR` format. It includes the name of the motif in the first line and
in the subsequent lines the counts of specific nucleotide at the given position are provided.

.. code-block:: text

  >MA0080.1	SPI1
  A  [    14      4      3     56     56      3 ]
  C  [    21      2      0      1      0     18 ]
  G  [    19     48     52      0      0     34 ]
  T  [     3      3      2      0      1      2 ]

To define such motif in the YAML specification, one needs to provide the path to the file where the motif is stored and
the threshold value - when matching the PWM to a sequence later, this is the threshold to consider the sequence as
containing the motif.

.. code-block:: yaml

  my_custom_pwm: # this will be the identifier of the motif
        file_path: my_pwm_1.jaspar
        threshold: 2

Position of the motif in the sequence
=======================================

LIgO supports the use of IMGT positions to specify where the motifs of one signal may occur in the sequence. To specify
the positions for the signal, one can define the position and the corresponding probability. For positions not explicitly
mentioned in the definition, the probability of the motifs occurring will be redistributed from remaining probability.
Specifically, for the example below, the motifs have the probability of 0.9 to occur at positions `109` and `110` and 0.1 total probability
to occur at any other position in the sequence. If some positions are explicitly not allowed, their probability can be
set to 0.

.. code-block:: yaml

    sequence_position_weights: # the motifs have the probability of 0.9 to occur at positions 109 and 110
        '109': 0.5
        '110': 0.4

User-defined functions for signal definition
==============================================

While the previously presented options allow for flexible definitions of motifs and signals, it is possible that the
user might have a different idea of how to define the signal. For that purpose, LIgO supports defining custom functions
that will for the given sequence return True/False based on whether the signal is in the sequence. For more details on
this option, see :ref:`Simulation with custom signal functions`.

Complete example of signal definition for receptor-level simulation
====================================================================

Here is an example of how a set of motifs can be defined and put together under `my_signal`.

.. code-block:: yaml

  motifs:
    my_simple_motif: # the name of the motif used for reference later
        seed: AAA # motif is always AAA
    my_gapped_motif: # the name of the more complex motif where / sign denotes a possible gap location
        seed: AA/A # this motif can be AAA, AA_A, CAA, CA_A, DAA, DA_A, EAA, EA_A
        min_gap: 0 # how many gaps can there be: min 0 and max 1
        max_gap: 1
        hamming_distance_probabilities: # it can have a max of 1 substitution
            0: 0.7
            1: 0.3
        position_weights: # note that index 2, the position of the gap, is excluded from position_weights
            0: 1 # only first position can be changed
            1: 0
            3: 0
        alphabet_weights: # the first A can be replaced by C, D or E
            C: 0.4
            D: 0.4
            E: 0.2
  signals:
    my_signal: # the name of the signal used for reference later in the simulation specification
        motifs:
            - my_simple_motif
            - my_gapped_motif
        sequence_position_weights:
            '109': 0.5
            '110': 0.4
        v_call: TRBV1
        j_call: TRBJ1

Here `my_signal` has two possible motifs that occur in IMGT positions `109` or `110` with probability 0.9 or in any
other position with probability 0.1, and that have to occur in combination with TRBV1 and TRBJ1 genes.

Repertoire-level simulation
=============================

In addition to the immune signal parameters described above, when defining the immune signal on the repertoire level,
we additionally provide the percentage of the
repertoire containing the given immune signal and the clonal frequency. Clonal frequency is modeled via zeta distribution
function from scipy and it is parameterized by shape parameter of the distribution (called `a` in scipy) and the `loc`
parameter that can be used to shift the distribution. Here is an example:

.. code-block:: yaml

  signals:
    my_signal: # same signal as before, with added clonal frequency parameters
        motifs:
            - my_simple_motif
            - my_gapped_motif
        sequence_position_weights:
            '109': 0.5
            '110': 0.5
        v_call: TRBV1
        j_call: TRBJ1
        clonal_frequency:
            a: 2
            loc: 0

Simulating immune events
==========================

We can define one or more signals as described above. If we want to combine multiple signals under a single label to
denote a single immune event (e.g., T1D disease state), LIgO supports this in the following way:

1. First all signals are defined,
2. The simulation configuration is provided that defines how the signals will be combined.

For each group of examples with the same parameters, we define the combination of signals under `signals` key. Then, for
that group, we assign the value of the label of interest. For example, to simulate a group of 30 type 1 diabetes (T1D)-specific
repertoires, where 20 repertoires have the disease and 10 do not, we may specify that positive repertoires contain
`my_signal`, but all of these repertoires contain `my_other_signal`, which could be specific to some other immune event
that is present in the full cohort. An example of such simulation configuration is provided below.

.. code-block:: yaml

  my_simulation_config:
    is_repertoire: true # we do repertoire-level simulation
    paired: false
    sequence_type: amino_acid
    simulation_strategy: RejectionSampling
    remove_seqs_with_signals: true # remove signal-specific AIRs from the background
    sim_items:
      t1d_positive_repertoires_group1: # group of AIRs with the same parameters
        generative_model:
          chain: beta
          default_model_name: humanTRB
          model_path: null
          type: OLGA
        number_of_examples: 10 # we simulate 10 repertoires
        receptors_in_repertoire_count: 100 # each repertoire has 100 receptors
        signals:
          my_signal: 0.1 # 10% of the receptors in the repertoire contain my_signal
          my_other_signal: 0.2 # 20% of the receptors contain my_other_signal
        immune_events:
          T1D: true
      t1d_positive_repertoires_group2: # group of AIRs with the same parameters
        generative_model:
          chain: beta
          default_model_name: humanTRB
          model_path: null
          type: OLGA
        number_of_examples: 10 # we simulate 10 repertoires
        receptors_in_repertoire_count: 100 # each repertoire has 100 receptors
        signals:
          my_signal: 0.15 # 15% of the receptors in the repertoire contain my_signal
          my_other_signal: 0.2 # 20% of the receptors contain my_other_signal
        immune_events:
          T1D: true
      t1d_negative_receptors:
        generative_model:
          chain: beta
          default_model_name: humanTRB
          model_path: null
          type: OLGA
        number_of_examples: 10 # we simulate 10 repertoires
        receptors_in_repertoire_count: 100 # each repertoire has 100 receptors
        signals:
          my_other_signal: 0.03 # 3% of the receptors contain my_other_signal but none contain my_signal
        immune_events:
          T1D: false

Immune events on the receptor level
*************************************

It is possible to define immune events in the same way on the receptor level. They could denote the same as on the
repertoire level: the disease state to which the signals listed are specific to, or some other label of interest, e.g.,
experiment or patient from which the receptor came from.

Next steps
============

For a full minimal working example, see the :ref:`Quickstart`. For detailed description of all the parameters and possible
values, see :ref:`YAML specification`. For help on choosing the content of the signals and motifs, see :ref:`How to check feasibility of the simulation parameters`.
For the discussion on defining immune events and signals in this way, see also `the LIgO manuscript <https://www.biorxiv.org/content/10.1101/2023.10.20.562936v2>`_.
