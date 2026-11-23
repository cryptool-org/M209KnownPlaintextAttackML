"""Regression test of both actual JSON exporters against simulator drum counts.

Run: python -B Tools/test_keystream_exporters.py
Optional: --repo PATH checks another tree; --expect-historical asserts the old bug.
Only temporary JSON files are created. No neural models or training are involved.
"""
import argparse
import importlib.util
import json
from pathlib import Path
import random
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--expect-historical', action='store_true')
    parser.add_argument('--temp-dir', type=Path, default=Path.cwd())
    args = parser.parse_args()
    repo = args.repo.resolve()
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(repo / 'm209 Brian Neal'))
    from m209.converter import M209
    from m209.keylist.generate import generate_key_list

    classes = []
    for name, cls in (('_3_encrypt', 'Encrypt'), ('_3_encrypt_sorted', 'EncryptSorted')):
        spec = importlib.util.spec_from_file_location(name, repo / 'Tools' / (name + '.py'))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        classes.append((name, getattr(module, cls)))

    cases, matching, historical_alignment, mismatches = 0, 0, 0, 0
    for seed in range(20):
        random.seed(seed)
        key = generate_key_list('AB', max_lug_attempts=10000)
        for length in (1, 10, 52, 104, 200, 500):
            for mixed in (False, True):
                plain = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ ') for _ in range(length)) if mixed else 'A' * length
                initial = 'BCDEFG' if mixed else 'AAAAAA'
                machine = M209()
                machine.set_drum_lugs(key.lugs)
                for n, pins in enumerate(key.pin_list):
                    machine.set_pins(n, pins)
                machine.set_key_wheels(initial)
                expected = []
                for _ in plain:
                    expected.append(machine.drum.rotate([w.is_effective() for w in machine.key_wheels]) % 26)
                    for wheel in machine.key_wheels:
                        wheel.rotate()
                for name, cls in classes:
                    with tempfile.TemporaryDirectory(dir=args.temp_dir.resolve()) as tmp:
                        enc = cls(destin_path=tmp + '/', count_a=length, append_keystream=True)
                        enc.keys = [[0, key.pin_list, key.lugs, key.letter_check]]
                        enc.set_int_msg_ind(initial)
                        if mixed:
                            enc.gutenberg_en = [plain]
                        if name == '_3_encrypt':
                            enc.encrypt('000_x')
                        else:
                            enc.encrypt_sorted('unused', '000_cipher.json')
                        row = json.loads((Path(tmp) / '000_cipher.json').read_text())[0]
                    stored = [ord(c)-65 for c in row[3]]
                    assert len(stored) == length
                    assert all(0 <= x < 26 for x in stored)
                    # Stored formatted ciphertext still includes both sets of indicators.
                    assert len(row[2].replace(' ', '')) == 20 + ((length+4)//5)*5
                    cases += 1
                    matching += stored == expected
                    mismatches += stored != expected
                    if args.expect_historical:
                        if not mixed and length > 10:
                            assert stored[10:] == expected[:-10]
                            historical_alignment += 1
                    else:
                        assert stored == expected, (name, seed, length, mixed)
    if args.expect_historical:
        assert mismatches > 0 and historical_alignment == 160
    print(json.dumps({'cases':cases, 'exact_matches':matching, 'mismatches':mismatches,
                      'historical_shift_checks':historical_alignment,
                      'mode':'historical negative control' if args.expect_historical else 'corrected regression',
                      'lengths':[1,10,52,104,200,500], 'seeds':20,
                      'plaintexts':['all A','mixed uppercase and spaces'],
                      'initial_positions':['AAAAAA','BCDEFG'],
                      'reference':'direct drum counts modulo 26, independently stepped wheels',
                      'neural_inference':False}, indent=2))


if __name__ == '__main__':
    main()
