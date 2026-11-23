# Known Plaintext Attack against Hagelin M-209 Cipher Machine using Aritificial Neural Networks

**Known issues (version of 2026-11-24).** The code and data in this repository, as used for our HistoCrypt 2024 paper, contain an error in the data preparation, and the paper contains several statements that go beyond what was measured. In short: (1) every input sequence starts with the 10 letters of the message indicator, so an input of length 52/104/200 contains only 42/94/190 keystream values (the published accuracies were measured with this input); (2) the available files document training and evaluation for wheel 1; (3) the published averages are over a class-stratified test set; (4) Table 1 of the paper differs slightly from the saved results in notebook #8, possibly because it came from a separate run. The method recovers part of the pins of one wheel; it is not a full key recovery. Details, the effect of each issue and the status of the correction: [KNOWN_ISSUES.md](KNOWN_ISSUES.md). The version used for the paper is preserved unchanged at tag `Tag-2026-11-12` ([Zenodo DOI](https://doi.org/10.5281/zenodo.24160196)). See the [reevaluation results](REEVALUATION_RESULTS.md).

## Overview

This project uses Machine Learning (ML),  specifically Artificial Neural Networks (ANNs), for cryptanalysis of the Hagelin M-209, a historical cipher machine. By analyzing pseudo-random displacement values (keystream) accessible from known ciphertext-plaintext pairs, our approach recovers parts of the secret key, focusing on the wheel pins settings. Each ANN takes as an input a fixed-length keystream and predicts one pin of a wheel. 

Regrettably, the same method cannot be straightforwardly applied to retrieve the other portion of the key, namely the bar-lugs positions. The reason is that each of the 27 bars contributes independently to the keystream generation process, and their effects are indistinguishable from one another. Consequently, swapping the settings of any two bar lugs does not alter the keystream production, resulting in a large set of functionally equivalent keys. Therefore, it becomes impractical to train a model to pinpoint a specific key value that would reveal the presence of a lug in a particular position against a wheel on the bar, due to the existence of numerous equivalent keys with contrary values. Hence, an alternative strategy must be considered, which currently remains under development.

The paper: V. Mikhalev, N. Kopal, B. Esslinger, H. Lampesberger, E. Hermann, "Cryptanalysis of Hagelin M-209 Cipher Machine with Artificial Neural Networks: A Known-Plaintext Attack", Proceedings of HistoCrypt 2024, NEALT Proceedings Series 53, [doi:10.58009/aere-perennius0108](https://doi.org/10.58009/aere-perennius0108). **Please also read the [known issues](KNOWN_ISSUES.md) and the [proposed paper corrections](PAPER_CORRECTION.md).**


## How the Code is Organized

Our project's code is in 8 Jupyter notebooks in the `Tools` folder, with each notebook serving a different purpose:

1. **#1_create_keys_train.ipynb**: Generates a collection of keys following the specifications outlined in the 1944 technical manual ([M209 manual](https://deweger.net/apparaten/downloads/M209%20manual.pdf)). This key set forms the basis for our training dataset.

2. **#2_create_ciphertexts_train.ipynb**: Produces JSON files that detail keys, keystreams, and ciphertexts derived from the training keys, creating the foundational training dataset for model development.

3. **#3_create_npy-data_train.ipynb**: Normalizes data arrays and converts them into `.npy` format for straightforward use as inputs and targets in model training.

4. **#4_train_models.ipynb**: Arranges the process of making and teaching the models with the training data.

5. **#5_create_keys_test.ipynb**:  Generates test keys, categorized based on their cryptographic strength, which is based on the number of non-shared and overlapping lugs. This nuanced approach facilitates a targeted analysis of model efficacy across varying scenarios.

6. **#6_create_ciphertexts_test.ipynb**: Similar to the training version but uses the test keys to prepare dataset for model evaluation

7. **#7_create_npy-data_test.ipynb**: Like its training analogue **#3_create_npy-data_train.ipynb**:, this notebook prepares normalized data arrays in `.npy` format, serving as inputs and targets for model evaluation.

8. **#8_test_models.ipynb**: Tests the trained models against the prepared test dataset, offering insights into performance metrics and model robustness in deciphering keys of differing cryptographic complexities.

## External Encryption Tool

For encrypting data, we use an external M-209 implementation found in Brian Neal's M-209 GitHub Repository. This tool is utilized for accurately simulating the encryption process as performed by the actual Hagelin M-209 machine. The original repository is accessible [here](https://github.com/gremmie/m209). Note that for data organizational reasons, we slightly modified some of this code. Therefore, for correct performance, please use the version available in the folder "m209 Brian Neal" of our repository.


## Getting Started

1. **Preparing Your Data**: Begin with our notebooks to generate ciphertext data. For a practical example, refer to the dataset used in our published attack available on [CrypTool Research Files](https://www.cryptool.org/en/research/). In the same location, our trained models are also available for download, allowing for direct application and further exploration.

2. **Training the Models**: Follow the steps in our training notebooks to develop and train your ANNs.

3. **Testing and Understanding Your Models**: Employ our evaluation notebook to test your models with fresh datasets and to derive insights from the results.

Check each Jupyter notebook and sequentially run them.
