"""Checks that the stored keystream equals the machine's displacement sequence.

Run from the Tools/ directory:  python test_keystream_alignment.py
Encrypts with the Encrypt class (as notebooks #2/#6 do: internal message
indicator AAAAAA, plaintext AAA...), then compares the stored keystream with
the displacements of an M-209 set to the same key and started at AAAAAA.
"""
import json
import random
import sys
import tempfile

sys.path.append("../m209 Brian Neal")

from m209.converter import M209
from m209.keylist.generate import generate_lugs, generate_pin_list, generate_letter_check
from _1_keygen_json import _lug_selection
from _3_encrypt import Encrypt

LENGTH = 200
TRIALS = 50

for trial in range(TRIALS):
    random.seed(trial)
    lugs = generate_lugs(lug_selection=_lug_selection(1, 12), max_attempts=10000)
    pins = generate_pin_list(max_attempts=10000)

    with tempfile.TemporaryDirectory() as d:
        enc = Encrypt(destin_path=d + "/", count_a=LENGTH, append_keystream=True)
        enc.keys = [[0, pins, lugs, generate_letter_check(lugs, pins)]]
        enc.set_int_msg_ind("AAAAAA")
        enc.encrypt("000_x")
        row = json.load(open(d + "/000_cipher.json"))[0]
    stored = [ord(ch) - ord("A") for ch in row[3]]

    m209 = M209()
    m209.set_drum_lugs(lugs)
    for n, p in enumerate(pins):
        m209.set_pins(n, p)
    m209.set_key_wheels("AAAAAA")
    ciphertext = m209.encrypt("A" * LENGTH, group=False)
    displacements = [(ord(c) - ord("A") + 1) % 26 for c in ciphertext]  # d = (c + p - 25) mod 26, p = 0

    assert len(stored) == LENGTH, (trial, len(stored))
    assert stored == displacements, "trial %d: stored keystream is not the displacement sequence" % trial

print("OK: in %d trials the stored keystream equals the displacement sequence (length %d)" % (TRIALS, LENGTH))
