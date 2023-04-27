YAML specification
###################

.. toctree::
   :maxdepth: 2

The YAML specification defines the simulation or analysis to be executed. The YAML contains the following sections:

- definitions: includes motifs, signals, and simulation details - these define conceptually what the user would like to simulate,
- instructions: cover the specific simulation or analysis to be run - usually including only technical information on how to perform the task and reference the components defined under definitions for the conceptual information;
- output: only HTML format is supported, and doesn't include any parameters.

The purpose of this page is to list all the YAML specification options.

The overall structure of the YAML specification is the following:

.. indent with spaces
.. code-block:: yaml

  definitions: # mandatory keyword
    motifs:
      my_motif_1: ...
    signals:
      my_sig_1: ...
    simulations:
      my_first_simulation: ...
  instructions: # mandatory keyword - at least one instruction has to be specified
    my_instruction_1: # user-defined name of the instruction
      ... # see below for the specification of different instructions
  output: # how to present the result after running (the only valid option now is HTML)
    format: HTML

Definitions
===========

Supported dataset formats
----------

.. include:: ./specs/definitions/datasets.rst

Simulation
----------

.. include:: ./specs/definitions/simulation.rst

Instructions
============

.. include:: ./specs/instructions/instructions.rst

