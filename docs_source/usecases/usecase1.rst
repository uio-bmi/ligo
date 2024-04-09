Manuscript use case 1: Out-of-distribution receptor-level simulation using LIgO
============================================================

The composition of train and test data can impact the quality and accuracy of AIRR-ML models. In our use case, we showed how splitting the train and test data may decrease predictive performance in out-of-distribution cases. With LIgO, we simulated a scenario where an immune signal is defined as one motif, but each individual carries a slightly different modification of this motif. 

We trained and evaluated a logistic regression model (LR) for receptor-level classification using two different train-test strategies. The first strategy involved a random split of all AIRs from all individuals into train and test sets, while the second strategy used a leave-one-individual-out approach, placing all AIRs from one individual into the test set and AIRs from the other individuals into the training set. Our findings revealed that LR trained on the random train-test strategy achieved higher balanced accuracy compared to LR trained on the leave-one-individual-out approach. 

In this tutorial, we give an example of a simulation configuration for a single dataset, along with detailed explanations of the parameters in the comments as needed. A detailed description of use case 1 can be found in the LIgO manuscript.

Simulation configuration
------------------------

.. image:: ../_static/figures/usecase1_signals.png
  :width: 500

ML configuration
-----------------

.. image:: ../_static/figures/usecase1_splits.png
  :width: 800
