# What we found / known issues

1. **Input data.** `Tools/_3_encrypt.py` (line 162) computes the "keystream" from the complete message that the simulator returns, including the 10 indicator letters at its start. So every input of length 52/104/200 contains only 42/94/190 keystream values. Our accuracies were measured on these inputs. The reevaluation of the original models gave accuracies close to the published figures. But the argument for the lengths 52 and 104 ("two/four full rotations") does not hold: with 42 values, ten pins of wheel 1 occur only once. The training log in notebook #4 shows this directly. These pins score about 62 %, the others about 67 %.
2. **The available notebooks document training and testing for wheel 1** (`pinwheel_sizes = [26]` in all training cells). The available files do not let us verify the earlier results for the smaller wheels.
3. **The averages** (71.91 / 88.40 / 96.71 %) are over a test set grouped by key class. Notebook #8 pools the test keys for the overall figures and uses up to 1000 keys per class for the per-class table. Separately, the training logs indicate about 65 % (n = 52) and 77 % (n = 104) on the internal test used during training. The rounding to 71 % and 96 % should be 72 % and 97 %.
4. **Table 1** is close to the saved results in notebook #8 but not the same. Of its 103 cells, 63 differ, by up to 2.8 percentage points. A separate run with different randomly generated or sampled test data could explain the difference. The [proposed correction](PAPER_CORRECTION.md) gives the table as it follows from notebook #8.
5. **Notebook #4 was edited after its run.** Two cells print results for a different sequence length than their code sets. Which training settings belong to which length is therefore not documented. The printed outputs show acceptance thresholds of 0.62, 0.77 and 0.88 for the three lengths.

   The published length-104 cell requests 10 files with up to 1,500 rows each. Both other lengths request 100 files, and the saved log for length 104 shows that 100 files were actually loaded. The original row limit per file is unknown. For the reevaluation, length 104 uses the same training-data amount as length 200 (100 files with up to 15,000 rows each) and keeps its own model and other training settings.  The [reevaluation results](REEVALUATION_RESULTS.md) describe the training and evaluation settings in detail.

6. **Wording.** The 13-lug example (p. 3) is wrong for the values 0, 1, 13 and 14. "Key-recovery attack" and "we can decrypt the remainder" go beyond what we did, since the lugs are not recovered. There is no comparison with Lasry et al. (2016a), which we cite.

**What is not affected.** No data were fabricated or altered. The networks do predict the pins of wheel 1 well above chance, and longer inputs gave higher accuracy in these runs. The available records do not show a comparison where length was the only setting changed. This is a case for a correction, not a retraction (COPE Retraction Guidelines, p. 4).

The 2024 models on [CrypTool Research Files](https://www.cryptool.org/en/research/) were trained on inputs with the 10 indicator values in front. After the fix, newly generated data no longer fit these models.

## Reusing archived data

The archived all-A ciphertext JSON files contain the faulty keystream. Anyone who wants to reuse *these* files without running notebooks #2/#6 again can skip the 10 values when converting them.

- `Tools/#3_create_npy-data_train.ipynb`, code cell 4, line 23 (raw file line 94);
- `Tools/#7_create_npy-data_test.ipynb`, code cell 3, line 23 (raw file line 80).

```python
        s=data[i][3][10:10+length]  # skip the 10 message-indicator values (KNOWN_ISSUES.md, issue 1)
```

Use this offset only on the archived all-A sequences. With the corrected exporters, take the first `length` values directly. See the [reevaluation results](REEVALUATION_RESULTS.md) for the original models and the new training.
