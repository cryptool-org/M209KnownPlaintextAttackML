# Proposed changes to the HistoCrypt 2024 paper

Sixteen changes, P1–P16, in page order. Severity: **E** = error of fact; **C** = claim not supported; **M** = minor.

### P1 – Abstract: "131 models" (C)
- **Where:** p. 1, left column, Abstract, lines 13–16 of the abstract (counted from "This paper introduces").
- **Before:** "Thus, to recover all the 131 pins, we utilize 131 models each solving a binary classification problem."
- **After:** "Each model solves a binary classification problem. The available files document training and evaluation of the 26 models for the pins of the first wheel."

### P2 – Abstract: input lengths (E)
- **Where:** p. 1, left column, Abstract, lines 16–18.
- **Before:** "By experimenting with various ANN architectures and ciphertext lengths, ranging from 52 to 200 characters, we identified an ANN architecture that outperforms others in accuracy."
- **After:** "By experimenting with various ANN architectures and input lengths of 52 to 200 values (because of an error in our data preparation, the first 10 of them were derived from the message-indicator letters, so the inputs contained 42 to 190 keystream values), we identified an ANN architecture that outperforms others in accuracy."

### P3 – Abstract: accuracies (E)
- **Where:** p. 1, left column, Abstract, lines 22–27.
- **Before:** "…achieved the following accuracies in recovering the pins of the first wheel of the machine: approximately 71% for 52-characters sequences, 88% for 104-characters, 96% for 200-characters."
- **After:** "…achieved the following average accuracies in recovering the pins of the first wheel of the machine, on a test set grouped by key class: about 72 % for inputs of 52 values, 88 % for 104 and 97 % for 200."

### P4 – Abstract: other wheels (C)
- **Where:** p. 1, left column, Abstract, lines 29–30.
- **Before:** "For the other wheels, these accuracies are slightly higher."
- **After:** *(delete the sentence)*

### P5 – Abstract: "key-recovery attack" (C)
- **Where:** p. 1, left column, Abstract, lines 30–33 (last sentence).
- **Before:** "To the best of our knowledge, this is the first time when ANNs are used in a key-recovery attack against such machines."
- **After:** "To the best of our knowledge, this is the first time ANNs are used to recover part of the key of such machines. The lugs are not recovered, and the method was not compared with the classical known-plaintext attack of Lasry et al. (2016a)."

### P6 – Section 3: displacement range (M)
- **Where:** p. 2, right column, lines 19–21.
- **Before:** "The displacement value di is determined by the number of shifted bars and can range from 0 to 27."
- **After:** "The displacement value di is determined by the number of shifted bars and can range from 0 to 27; Equation 1 reveals only di mod 26, so 0 and 26, and 1 and 27, cannot be told apart."

### P7 – Section 4: 131 classifiers (C)
- **Where:** p. 2, right column, Section 4, lines 9–12 of the section (column lines 39–42).
- **Before:** "Therefore, 131 binary classifier models that share the same ANN architecture are used to predict the states of all pins."
- **After:** "Therefore, 131 binary classifier models that share the same ANN architecture would predict the states of all pins. The available files document training and evaluation of the 26 models for the first wheel."

### P8 – Section 4: definition of equivalent keys (M)
- **Where:** p. 2, right column, Section 4, lines 13–15 of the section (column lines 43–45).
- **Before:** "If different keys used in a cipher for encrypting the same plaintext lead to the same ciphertext, these keys are called equivalent."
- **After:** "If different keys produce the same ciphertext for every plaintext, these keys are called equivalent."

### P9 – Section 4: decryption (C)
- **Where:** p. 3, left column, lines 6–8.
- **Before:** "When such an equivalent key is found, we can decrypt the remainder of the ciphertext without the need for plaintext."
- **After:** "If an equivalent key, including the lugs, were found, the remainder of the ciphertext could be decrypted without plaintext. Our method recovers only pins, not the lugs."

### P10 – Section 4: input lengths and rotations (E)
- **Where:** p. 3, left column, lines 11–21.
- **Before:** "Utilizing these keys, we created sequences of displacement values which are 52, 104, and 200 numbers long. The choice of length 52 ensures that the first wheel completes two full rotations, such that every pin contributed at least twice in the displacement generation process. Similarly, length 104 corresponds to four full rotations. In experiments, this approach led to a slight but noticeable improvement in accuracy compared to sequences of 50 and 100 characters."
- **After:** "Utilizing these keys, we created input sequences which are 52, 104, and 200 numbers long. Because of an error in our data preparation, the first 10 numbers of every sequence were derived from the 10 message-indicator letters at the start of the message, not from the keystream. The sequences therefore contained only 42, 94 and 190 displacement values. The lengths 52 and 104 had been chosen so that every pin of the first wheel would contribute at least twice (52) or four times (104). With 42 values, ten pins of the first wheel contribute only once. The slight improvement over sequences of 50 and 100 characters observed in our experiments therefore cannot be explained by complete rotations."

### P11 – Section 5: other wheels (C)
- **Where:** p. 3, right column, Section 5, first paragraph, last sentence (lines 8–9 of the section).
- **Before:** "The results for the other wheels are marginally better."
- **After:** "The available files do not let us verify the earlier results for the smaller wheels."

### P12 – Section 5: test set (E)
- **Where:** p. 3, right column, Section 5, lines 10–11.
- **Before:** "For testing, we generated 1000 random keys for each of the key classes…"
- **After:** "For testing, we generated up to 1000 random keys for each of the 103 key classes for the per-class table (99,903 tests in total; seven classes have fewer than 1000)…"
- **Add at the end of that paragraph:** "The per-class table uses up to 1000 tests per class. The overall figures pool the test keys across classes."

### P13 – Section 5: the 13-lug example (E)
- **Where:** p. 3, right column, Section 5, lines 19–22, and footnote 6.
- **Before:** "In this case, if the total displacement value is between 15 and 25, it guarantees that the current pin of this wheel is active; otherwise, it's inactive."
- **After:** "In this case, an observed displacement value between 15 and 25 guarantees that the current pin of this wheel is active, and a value between 2 and 12 that it is inactive. The values 0, 1, 13 and 14 can occur in both cases, because the other 14 bars add between 0 and 14 to the displacement."
- Footnote 6 can stay.

### P14 – Section 5: averages and the effect of length (E, C)
- **Where:** p. 3, right column, last line ("In"), continued on p. 4, left column, lines 1–7 below Figure 3.
- **Before:** "In terms of average accuracy, sequences of 52 characters yield 71%, those with 104 characters reach 88%, and for sequences encompassing 200 characters, the accuracy stands at 96%. This behavior was expected because longer displacement sequences carry more information and the average accuracy therefore increases."
- **After:** "In terms of average accuracy over the test keys, sequences of 52 values yield 72 %, those with 104 values reach 88 %, and for sequences of 200 values, the accuracy stands at 97 %. Longer inputs gave higher accuracy. The available records do not show a comparison where length was the only setting changed."

### P15 – Table 1 and its caption (E)
- **Where:** p. 4, right column, Table 1 (lines 23–42), and the reference to it on p. 4, left column, lines 11–13 below Figure 3 ("The results related … are shown in Table 1.").
- **Before:** the published Table 1.
- **After:** replace the table with the values saved in notebook #8 (`check6_table1_from_notebook8.py`). The published values are very close. A separate run with different randomly generated or sampled test data could explain the difference. The values are rounded half up; `*` marks the 63 changed cells (`*` is not part of the table).

```
N\O    0    1    2    3    4    5    6    7    8    9   10   11   12
  0    -  52*  51   54*  56*  58*  59*  60*  62*  63   65   66*  69*
  1  55*  54   56*  57   60*  62*  63*  65*  65   67*  69*  70*  72*
  2  55   57   59   62*  63*  64   66*  68*  68   69   71*  73*    -
  3  59   61*  62   64   66   69*  70*  71*  72*  73*  74     -    -
  4  62*  64   66   68   70   72   74*  74*  75*  76*    -    -    -
  5  67*  69   70   72   74*  75*  77*  78*  79*    -    -    -    -
  6  70*  72*  74*  75   77*  79*  81*  82*    -    -    -    -    -
  7  73   75   77*  79   82   83*  85*    -    -    -    -    -    -
  8  77*  79*  82*  84*  86*  88*    -    -    -    -    -    -    -
  9  81   84*  86*  88*  89     -    -    -    -    -    -    -    -
 10  85   87   89   91*    -    -    -    -    -    -    -    -    -
 11  88   90   92     -    -    -    -    -    -    -    -    -    -
 12  91   93     -    -    -    -    -    -    -    -    -    -    -
 13  94*    -    -    -    -    -    -    -    -    -    -    -    -
```

- **Caption, before:** "Table 1: Mean accuracy in % for the different number of non-shared lugs (represented by rows) and overlaps (represented by columns). These results are for sequences of 52 characters long."
- **Caption, after:** "Table 1: Mean accuracy in % for the different number of non-shared lugs (rows) and overlaps (columns), for input sequences of 52 values (42 keystream values), from the per-class results saved in notebook #8. Each cell is based on 1000 tests, except NS=0/OV=9–12 (568, 375, 602, 202), NS=1/OV=11–12 (957, 416) and NS=2/OV=11 (783)."
- **Note on the count:** earlier documents count 62 differing cells (61 lower, 1 higher). The difference is a single cell, NS=5/OV=0 = 66.50 %. Python's `round()` gives 66 there, the same as the published table; conventional rounding gives 67. So 63 cells differ.

### P16 – Conclusion (C)
- **Where:** p. 4, left column, last line ("ANN architectures, particularly a custom ResNet-"), continued on p. 4, right column, first two lines below Table 1.
- **Before:** "Our experiments with various ANN architectures, particularly a custom ResNet-like model, highlight the effectiveness of ML in the cryptanalysis of such machines."
- **After:** "Our experiments with various ANN architectures, particularly a custom ResNet-like model, show that ANNs can recover a substantial part of the pins of the first wheel from short known-plaintext segments."
