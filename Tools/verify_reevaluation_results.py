"""Check the reported counts; optionally verify locally retained predictions/models.

python Tools/verify_reevaluation_results.py
python Tools/verify_reevaluation_results.py --labels path/to/y.npy --artifacts-root path/to/artifacts --verify-models
The optional artifact check needs NumPy. No training or files are changed.
"""
import argparse
import hashlib
import json
from pathlib import Path


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def close(a, b):
    assert abs(a-b)<1e-9, (a,b)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--labels', type=Path)
    parser.add_argument('--artifacts-root', type=Path)
    parser.add_argument('--verify-models', action='store_true')
    args = parser.parse_args()
    if bool(args.labels)!=bool(args.artifacts_root) or (args.verify_models and not args.artifacts_root):
        parser.error('--labels and --artifacts-root are required together; --verify-models also needs them.')
    results = Path(__file__).resolve().parents[1]/'results'
    manifest = read(results/'corrected-training-results.json')
    rescoring = read(results/'wheel-1-rescoring.json')
    first = read(results/'first-pass-verification.json')
    cases = manifest['test_cases']
    assert cases==rescoring['test_keys']==first['archived_test_cases']==102976
    assert set(manifest['lengths'])==set(rescoring['lengths'])==set(first['lengths'])=={'52','104','200'}
    assert first['verified_predictions_and_scores']==78
    assert manifest['archived_labels_sha256']==rescoring['archived_label_file_sha256']
    if args.labels:
        import numpy as np
        assert digest(args.labels)==manifest['archived_labels_sha256']
        labels = np.load(args.labels, mmap_mode='r')
        assert labels.shape==(cases,131)
        artifact_root = args.artifacts_root.resolve()
    summary = {}
    arrays_checked = models_checked = 0
    for length in ('52','104','200'):
        g = manifest['lengths'][length]
        assert [p['pin_number'] for p in g['pins']]==list(range(1,27))
        assert [p['label_column'] for p in g['pins']]==list(range(26))
        assert g['models_trained_and_evaluated']==26
        for kind in ('original_2024','corrected_first_attempt'):
            d = rescoring['lengths'][length][kind]
            assert d['pin_numbers_1_based']==list(range(1,27))
            assert len(d['correct_predictions_per_pin'])==26
            assert all(isinstance(v,int) and 0<=v<=cases for v in d['correct_predictions_per_pin'])
            assert d['correct_predictions']==sum(d['correct_predictions_per_pin'])
            assert d['total_predictions']==26*cases
            close(d['accuracy_percent'],100*d['correct_predictions']/d['total_predictions'])
        original = rescoring['lengths'][length]['original_2024']
        corrected = rescoring['lengths'][length]['corrected_first_attempt']
        counts = [p['correct_predictions'] for p in g['pins']]
        assert counts==corrected['correct_predictions_per_pin']
        assert sum(counts)==g['correct_pin_predictions']==first['lengths'][length]['1']['correct_pin_predictions']
        close(g['accuracy_percent'],100*sum(counts)/(26*cases))
        close(g['accuracy_percent'],first['lengths'][length]['1']['external_accuracy_percent'])
        close(g['original_model_accuracy_percent'],original['accuracy_percent'])
        close(g['difference_from_original_pp'],g['accuracy_percent']-original['accuracy_percent'])
        all_correct = []
        for p in g['pins']:
            close(p['accuracy_percent'],100*p['correct_predictions']/cases)
            if args.labels:
                path = (artifact_root/p['probabilities_file']).resolve()
                assert path.is_relative_to(artifact_root)
                assert digest(path)==p['probabilities_sha256']
                probabilities = np.load(path, mmap_mode='r')
                assert probabilities.shape==(cases,) and np.isfinite(probabilities).all()
                assert probabilities.min()>=0 and probabilities.max()<=1
                correct = np.rint(probabilities)==labels[:,p['label_column']]
                assert int(correct.sum())==p['correct_predictions']
                all_correct.append(correct)
                arrays_checked += 1
                if args.verify_models:
                    model = (artifact_root/p['model_file']).resolve()
                    assert model.is_relative_to(artifact_root) and digest(model)==p['model_sha256']
                    models_checked += 1
        if args.labels:
            assert int(np.column_stack(all_correct).all(axis=1).sum())==g['exact_wheel_correct']
        summary[length] = dict(accuracy_percent=g['accuracy_percent'], trained_and_evaluated=26)
    print(json.dumps(dict(counts_reconciled=True, prediction_arrays_verified=arrays_checked,
                          model_hashes_verified=models_checked, lengths=summary),indent=2))


if __name__=='__main__':
    main()
