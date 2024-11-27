Overview of LIgO simulation parameters 
=========================================

This page provides an overview of LIgO simulation parameters and their potential biological reflection. Refers to Supplementary Table 2 in the LIgO manuscript.

Generative models for simulation of background AIRs
-----------------------------
Link to documentation: 

- https://uio-bmi.github.io/ligo/specification.html#experimentalimport

.. list-table:: 
  :header-rows: 1

  * - Simulation parameter(s)
    - Potential biological reflection
  * - **ExperimentalImport** provides import of existing experimental data of one of the following data formats: AIRR, Generic, IGoR, IReceptor, ImmuneML, ImmunoSEQRearrangement, ImmunoSEQSample, MiXCR, OLGA, SingleLineReceptor, TenxGenomics, VDJdb 
    - These parameters relate biologically to germline gene usage differences across individuals as previously shown by us and others (Glanville et al. 2011; Slabodkin et al. 2021).
  * - **OLGA** provides simulation of synthetic AIRs using a V(D)J recombination model, including a user-defined custom model 
    - Same as above

Motif definition
-----------------------------
Links to documentation: 

- https://uio-bmi.github.io/ligo/specification.html#seedmotif

- https://uio-bmi.github.io/ligo/specification.html#pwm

.. list-table:: 
  :header-rows: 1

  * - Simulation parameter(s)
    - Potential biological reflection
  * - **SeedMotif** describes a motif using a (i) **seed** (the initial k-mer) and (ii) allowed deviations from the seed. The allowed deviations can be described with allowed gap length (**min_gap**, **max_gap**), distribution of number of allowed mismatches to the seed (**hamming_distance_probabilities**), distribution of mismatches across the seed positions (**position_weights**), and substitution probabilities for nucleotides or amino acid (**alphabet_weights**). 
    - Can be used to describe antigen-binding motifs, which are present in signal-specfic AIRs as was previously observed by us and others (Akbar et al. 2021; Shrock et al. 2023; Ostmeyer et al. 2019; Shugay et al. 2018; Goncharov et al. 2022; Chronister et al. 2021)
  * - **PWM** — motif described in a form of a positional weight matrix
    - Same as above

Signal definition
-----------------------------
Link to documentation: 

- https://uio-bmi.github.io/ligo/specification.html#signal

.. list-table:: 
  :header-rows: 1

  * - Simulation parameter(s)
    - Potential biological reflection
  * - **Motifs** — several motifs within an immune signal  
    - Relates to motifs co-occurrence within the same AIR (2 motifs max), since immune signals may comprise multiple co-occurring motifs within the same AIR (Akbar et al. 2021; Glanville et al. 2017; Dash et al. 2017)
  * - **Sequence_position_weights** describes signal distribution across CDR3 IMGT positions  
    - Helps preserve the conservative start and end of CDR3, and controls a motif predominance in a specific location within CDR3
  * - **V_call**, **J_call** restrict the V or J gene (allele) in the immune signal  
    - Relates to previous observations that some signal-specific AIRs are associated with a specific germline gene alleles (Feeney et al. 1996; Avnir et al. 2016; Liu and Lucas 2003; Imkeller et al. 2018; Fagiani, Catanzaro, and Lanni 2020)  
  * - **Clonal_frequency** describes clonal frequency distribution, can be defined separately for each group of immune signals   
    - Relates to previous observation by us and others that clonal frequency distributions may change across immune statuses (Greiff et al. 2015; Chiffelle et al. 2020).
  * - Custom signal function (**source_file**, **is_present_func**) — any user-defined function which takes as arguments motifs, v_call, j_call, and sequence_position_weights 
    - Helps to define any custom immune signal


Parameters related to a group of receptors or repertoires 
-----------------------------
Link to documentation: 

- https://uio-bmi.github.io/ligo/specification.html#simulation-config-item

.. list-table:: 
  :header-rows: 1

  * - Simulation parameter(s)
    - Potential biological reflection
  * - **Signals** — distribution of signals across the simulated AIRs
    - Helps increase complexity of simulated data
  * - **Is_noise** indicates if a group of signal-specific AIRs should be labeled as not signal-specific 
    - Relates to experimental artifacts that may occur under imperfect experimental conditions
  * - **Generative_model** defines V(D)J model for a given set of AIRs 
    - Helps increase complexity of simulated data and control gene allele distribution of signal-specific AIRs
  * - **False_positives_prob_in_receptors**, **false_negative_prob_in_receptors** percentage of false positive or false negative AIRs when performing repertoire-level simulation 
    - Relates to experimental artifacts that may occur under imperfect experimental conditions
  * - **Immune_events** — receptor or repertoire-level labels, which can be later used for AIRR-ML
    - Relates to  diseases, vaccinations, allergies, etc,   which elicit immune responses 
  * - **Default_clonal_frequency** — clonal frequency distribution for background AIRs
    - Relates to previous observation by us and others that clonal frequency distributions may change across immune statuses (Greiff et al. 2015; Chiffelle et al. 2020).
  * - **Sequence_len_limits** restricts minimal and maximal CDR3 lengths to be included in the simulated data
    - Relates to length biases observed in signal-specific AIRs (Haakenson, Huang, and Smider 2018; Roark et al. 2021)


Parameters of the simulation
-----------------------------
Link to documentation: 

- https://uio-bmi.github.io/ligo/specification.html#simulation-config

.. list-table:: 
  :header-rows: 1

  * - Simulation parameter(s)
    - Potential biological reflection
  * - **Is_repertoire** defines receptor or repertoire level of simulation
    - Relates to different types of available AIRR data
  * - **Paired** defines how to pair the output data 
    - Relates to different types of available AIRR data
  * - **Sequence_type** — defines the nucleotide or amino acid type of simulated AIRs
    - Relates to different types of available AIRR data
  * - **Species** — human (default) or mouse
    - Relates to different types of available AIRR data
  * - **Keep_p_gen_dist** implements importance sampling, i.e., subsample signal-specific AIRs with respect to pgen distribution of background AIRs 
    - Relates to previous observations by us and other that found marked differences in pgen and clonal frequency which may relate to immune signal (Kanduri et al. 2023; Pogorelyy et al. 2019) 
  * - **Remove_seqs_with_signals** filters signal-specific AIRs from the background if True
    - Helps to control the exact number of signal-specific receptors within a set of AIRs (if True) or make simulated data more complex (if False)

References
-----------------------------

- Akbar, Rahmad, Philippe A. Robert, Milena Pavlović, Jeliazko R. Jeliazkov, Igor Snapkov, Andrei Slabodkin, Cédric R. Weber, et al. 2021. “A Compact Vocabulary of Paratope-Epitope Interactions Enables Predictability of Antibody-Antigen Binding.” Cell Reports 34 (11): 108856.

- Avnir, Yuval, Corey T. Watson, Jacob Glanville, Eric C. Peterson, Aimee S. Tallarico, Andrew S. Bennett, Kun Qin, et al. 2016. “IGHV1-69 Polymorphism Modulates Anti-Influenza Antibody Repertoires, Correlates with IGHV Utilization Shifts and Varies by Ethnicity.” Scientific Reports 6 (February):20842.

- Chiffelle, Johanna, Raphael Genolet, Marta As Perez, George Coukos, Vincent Zoete, and Alexandre Harari. 2020. “T-Cell Repertoire Analysis and Metrics of Diversity and Clonality.” Current Opinion in Biotechnology 65 (October):284–95.

- Chronister, William D., Austin Crinklaw, Swapnil Mahajan, Randi Vita, Zeynep Koşaloğlu-Yalçın, Zhen Yan, Jason A. Greenbaum, et al. 2021. “TCRMatch: Predicting T-Cell Receptor Specificity Based on Sequence Similarity to Previously Characterized Receptors.” Frontiers in Immunology 12 (March):640725.

- Dash, Pradyot, Andrew J. Fiore-Gartland, Tomer Hertz, George C. Wang, Shalini Sharma, Aisha Souquette, Jeremy Chase Crawford, et al. 2017. “Quantifiable Predictive Features Define Epitope-Specific T Cell Receptor Repertoires.” Nature 547 (7661): 89–93.

- Fagiani, Francesca, Michele Catanzaro, and Cristina Lanni. 2020. “Molecular Features of IGHV3-53-Encoded Antibodies Elicited by SARS-CoV-2.” Signal Transduction and Targeted Therapy 5 (1): 170.

- Feeney, A. J., M. J. Atkinson, M. J. Cowan, G. Escuro, and G. Lugo. 1996. “A Defective Vkappa A2 Allele in Navajos Which May Play a Role in Increased Susceptibility to Haemophilus Influenzae Type B Disease.” The Journal of Clinical Investigation 97 (10): 2277–82.

- Glanville, Jacob, Huang Huang, Allison Nau, Olivia Hatton, Lisa E. Wagar, Florian Rubelt, Xuhuai Ji, et al. 2017. “Identifying Specificity Groups in the T Cell Receptor Repertoire.” Nature 547 (June):94–98.

- Glanville, Jacob, Tracy C. Kuo, H-Christian von Büdingen, Lin Guey, Jan Berka, Purnima D. Sundar, Gabriella Huerta, et al. 2011. “Naive Antibody Gene-Segment Frequencies Are Heritable and Unaltered by Chronic Lymphocyte Ablation.” Proceedings of the National Academy of Sciences of the United States of America 108 (50): 20066–71.

- Goncharov, Mikhail, Dmitry Bagaev, Dmitrii Shcherbinin, Ivan Zvyagin, Dmitry Bolotin, Paul G. Thomas, Anastasia A. Minervina, et al. 2022. “VDJdb in the Pandemic Era: A Compendium of T Cell Receptors Specific for SARS-CoV-2.” Nature Methods 19 (9): 1017–19.

- Greiff, Victor, Pooja Bhat, Skylar C. Cook, Ulrike Menzel, Wenjing Kang, and Sai T. Reddy. 2015. “A Bioinformatic Framework for Immune Repertoire Diversity Profiling Enables Detection of Immunological Status.” Genome Medicine 7 (1): 49.

- Haakenson, Jeremy K., Ruiqi Huang, and Vaughn V. Smider. 2018. “Diversity in the Cow Ultralong CDR H3 Antibody Repertoire.” Frontiers in Immunology 9 (June):1262.

- Imkeller, Katharina, Stephen W. Scally, Alexandre Bosch, Gemma Pidelaserra Martí, Giulia Costa, Gianna Triller, Rajagopal Murugan, et al. 2018. “Antihomotypic Affinity Maturation Improves Human B Cell Responses against a Repetitive Epitope.” Science 360 (6395): 1358–62.

- Kanduri, Chakravarthi, Lonneke Scheffer, Milena Pavlović, Knut Dagestad Rand, Maria Chernigovskaya, Oz Pirvandy, Gur Yaari, Victor Greiff, and Geir K. Sandve. n.d. “simAIRR: Simulation of Adaptive Immune Repertoires with Realistic Receptor Sequence Sharing for Benchmarking of Immune State Prediction Methods.” GigaScience. https://doi.org/10.1093/gigascience/giad074.

- Liu, Leyu, and Alexander H. Lucas. 2003. “IGH V3-23*01 and Its Allele V3-23*03 Differ in Their Capacity to Form the Canonical Human Antibody Combining Site Specific for the Capsular Polysaccharide of Haemophilus Influenzae Type B.” Immunogenetics 55 (5): 336–38.

- Ostmeyer, Jared, Scott Christley, Inimary T. Toby, and Lindsay G. Cowell. 2019. “Biophysicochemical Motifs in T-Cell Receptor Sequences Distinguish Repertoires from Tumor-Infiltrating Lymphocyte and Adjacent Healthy Tissue.” Cancer Research 79 (7): 1671–80.

- Pogorelyy, Mikhail V., Anastasia A. Minervina, Mikhail Shugay, Dmitriy M. Chudakov, Yuri B. Lebedev, Thierry Mora, and Aleksandra M. Walczak. 2019. “Detecting T Cell Receptors Involved in Immune Responses from Single Repertoire Snapshots.” PLoS Biology 17 (6): e3000314.

- Roark, Ryan S., Hui Li, Wilton B. Williams, Hema Chug, Rosemarie D. Mason, Jason Gorman, Shuyi Wang, et al. 2021. “Recapitulation of HIV-1 Env-Antibody Coevolution in Macaques Leading to Neutralization Breadth.” Science 371 (6525). https://doi.org/10.1126/science.abd2638.

- Sethna, Zachary, Yuval Elhanati, Curtis G. Callan, Aleksandra M. Walczak, and Thierry Mora. 2019. “OLGA: Fast Computation of Generation Probabilities of B- and T-Cell Receptor Amino Acid Sequences and Motifs.” Bioinformatics. https://doi.org/10.1093/bioinformatics/btz035.

- Shrock, Ellen L., Richard T. Timms, Tomasz Kula, Elijah L. Mena, Anthony P. West Jr, Rui Guo, I-Hsiu Lee, et al. 2023. “Germline-Encoded Amino Acid-Binding Motifs Drive Immunodominant Public Antibody Responses.” Science 380 (6640): eadc9498.

- Shugay, Mikhail, Dmitriy V. Bagaev, Ivan V. Zvyagin, Renske M. Vroomans, Jeremy Chase Crawford, Garry Dolton, Ekaterina A. Komech, et al. 2018. “VDJdb: A Curated Database of T-Cell Receptor Sequences with Known Antigen Specificity.” Nucleic Acids Research 46 (D1): D419–27.

- Slabodkin, Andrei, Maria Chernigovskaya, Ivana Mikocziova, Rahmad Akbar, Lonneke Scheffer, Milena Pavlović, Habib Bashour, et al. 2021. “Individualized VDJ Recombination Predisposes the Available Ig Sequence Space.” Genome Research, November. https://doi.org/10.1101/gr.275373.121.




