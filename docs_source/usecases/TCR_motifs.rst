Constructing LIgO motifs inspired by VDJdb
===================================================

LIgO enables the generation of motifs based on either a PSSM or a combination of a short amino acid sequence (i.e., a seed) and a list of hamming distances. When starting from a known sequence motif present in a group of TCRs, a PSSM can be used. However, when the exact distribution of every amino acid is unknown, the simpler method of defining a seed and distances is recommended.
 
When defining the LIgO seeds, it is important to take into account the influence of the seed length and hamming distances on the quality of the simulated TCR sequences. Ideally, when simulating a TCR repertoire or a list of TCR sequences, the predefined LIgO seeds must be identifiable within these TCRs.
 
In this tutorial, we demonstrate the influence of the length of the seed and the simulated TCR repertoires. To this end, two epitope-specific TCR repertoires were generated as explained in (refer to the main tutorial on epitope-specific TCR simulations). Both simulations started from three seeds, each derived from one TCR in the VDJdb recognizing the DENV3/4 epitope GTSGSPIINR (Table 1). The first simulation was carried out using seeds of eight amino acids. In the second simulation, the seeds were only three amino acids long. All other simulation parameters were kept identical. The simulation results can be found here.

.. list-table:: Description of the long and short seeds
   :header-rows: 1

  * - TCR beta sequence
    - TRBV gene
    - TRBJ gene
    - Epitope
    - Long Seed
    - Short Seed
  * - CSVELSGINQPQHF
    - TRBV29-1
    - TRBJ1-5
    - GTSGSPIINR
    - ELSGINQP
    - SGI
  * - CASSPAGGTYEQYF
    - TRBV11-2
    - TRBJ2-7
    - GTSGSPIINR
    - SPAGGTYE
    - PAG
  * - CASSGGDVREEQYF
    - TRBV9
    - TRBJ2-7
    - GTSGSPIINR
    - SGGDVREE
    - DVR







