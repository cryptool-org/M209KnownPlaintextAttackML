# What we found / known issues

1. **Input data.** `Tools/_3_encrypt.py` (line 162) computes the "keystream" from the complete message that the simulator returns, including the 10 indicator letters at its start. So every input of length 52/104/200 contains only 42/94/190 keystream values. Our accuracies were measured on these inputs and are, if anything, slightly too low. But the argument for the lengths 52 and 104 ("two/four full rotations") does not hold: with 42 values, ten pins of wheel 1 occur only once. The training log in notebook #4 shows this directly. These pins score about 62 %, the others about 67 %.
2. **Only wheel 1 was trained and tested** (`pinwheel_sizes = [26]` in all training cells). "131 models" and "for the other wheels, these accuracies are slightly higher" have no experiment behind them.
3. **The averages** (71.91 / 88.40 / 96.71 %) are over a test set with (about) 1000 keys per key class, so all classes count equally. For keys drawn as in the 1944 rules, the training logs indicate about 65 % (n = 52) and 77 % (n = 104). The rounding to 71 % and 96 % should be 72 % and 97 %.
4. **Table 1** does not come from the evaluation run in notebook #8, which Figure 2 matches exactly. 63 of its 103 cells differ, by up to 2.8 points. I attach the table as it follows from notebook #8.
5. **Notebook #4 was edited after its run.** Two cells print results for a different sequence length than their code sets. Which training settings belong to which length is therefore not documented. The printed outputs show acceptance thresholds of 0.62, 0.77 and 0.88 for the three lengths.
6. **Wording.** The 13-lug example (p. 3) is wrong for the values 0, 1, 13 and 14. "Key-recovery attack" and "we can decrypt the remainder" go beyond what we did, since the lugs are not recovered. There is no comparison with Lasry et al. (2016a), which we cite.

**What is not affected.** No data were fabricated or altered. The networks do predict the pins of wheel 1 well above chance, and longer inputs do give higher accuracy. This is a case for a correction, not a retraction (COPE Retraction Guidelines, p. 4).

The 2024 models on Google Drive were trained on inputs with the 10 indicator values in front. After the fix, newly generated data no longer fit these models.

## Reusing archived data

The ciphertext JSON files on Google Drive contain the faulty keystream. Anyone who wants to reuse *these* files without running notebooks #2/#6 again can skip the 10 values when converting them.

- `Tools/#3_create_npy-data_train.ipynb`, code cell 4, line 23 (raw file line 94);
- `Tools/#7_create_npy-data_test.ipynb`, code cell 3, line 23 (raw file line 80).

```python
        s=data[i][3][10:10+length]  # skip the 10 message-indicator values (KNOWN_ISSUES.md, issue 1)
```
