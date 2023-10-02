# LIgO


![Python application](https://github.com/uio-bmi/ligo/workflows/Python%20application/badge.svg?branch=main)
![Docker](https://github.com/uio-bmi/ligo/workflows/Docker/badge.svg?branch=main)

LIgO is a tool for simulation of adaptive immune receptors and repertoires, 
internally powered by [immuneML](https://immuneml.uio.no/). The README includes quick installation instructions and information on how to run a quickstart. For more detailed documentation, see https://uio-bmi.github.io/ligo/.

## Installation

Requirements: Python 3.11 or later.

To install from PyPI (recommended), run the following command in your virtual environment:
```
pip install ligo
```
To install LIgO from the repository, run the following:
```
pip install git+https://github.com/uio-bmi/ligo.git
```
To be able to use Stitcher to export full-length sequences, download the database after installing LIgO:
```
stitchrdl -s human
```

## Usage

To run LIgO simulation, it is necessary to define the YAML file describing the simulation. Here is
an example YAML specification, that will create 300 T-cell receptors. The first 100
receptors will contain signal1 (which means all of these 100 receptors will have TRBV7 gene and `AS` 
somewhere in the receptor sequence), the next 100 receptors will contain signal2 (sequences will contain `G/G`
with the gap denoted by '\' sign and the gap size between 1 and 2 inclusive), and the final 100 receptors
will not contain any of these signals.

```yaml
definitions:
  motifs:
    motif1:
      instantiation: GappedKmer
      seed: AS # any k-mer
    motif2:
      instantiation:
        GappedKmer:
          max_gap: 2
          min_gap: 1
      seed: G/G
  signals:
    signal1:
      v_call: TRBV7
      motifs:
      - motif1
    signal2:
      motifs:
      - motif2
  simulations:
    sim1:
      is_repertoire: false
      paired: false
      sequence_type: amino_acid
      simulation_strategy: RejectionSampling
      sim_items:
        sim_item1: # group of sequences with same simulation params
          generative_model:
            chain: beta
            default_model_name: humanTRB
            model_path: null
            type: OLGA
          number_of_examples: 100
          seed: 1002
          signals:
           signal1: 1
        sim_item2: # second group of sequences with same simulation params
          generative_model:
            chain: beta
            default_model_name: humanTRB
            model_path: null
            type: OLGA
          number_of_examples: 100
          seed: 2
          signals:
            signal2: 1 # all receptors will have the signal
        sim_item3: # third group of sequences with same simulation params
          generative_model:
            chain: beta
            default_model_name: humanTRB
            model_path: null
            type: OLGA
          number_of_examples: 100
          seed: 5231
          signals: {} # no signal -> background sequences
instructions:
  my_sim_inst:
    export_p_gens: false # could take some time to compute
    max_iterations: 100
    number_of_processes: 4
    sequence_batch_size: 1000
    simulation: sim1
    store_signal_in_receptors: true
    type: LigoSim
```

To run this simulations, save the YAML file above as specs.yaml and run the following:

```commandline
ligo specs.yaml output_folder
```

Note that `output_folder` (user-defined name) should not exist before the run.
