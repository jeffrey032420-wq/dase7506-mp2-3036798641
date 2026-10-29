"""Use arithmetic-aware ranking only where explicit arithmetic conflicts exist."""
import json
from pathlib import Path
import numpy as np
from method_round2 import score as baseline_scores
from method_round7_v3 import candidate_scores as numeric_scores
from numeric_round7_v3 import build


def gate_mask(bank):
    return (build(bank).reshape(len(bank),4,-1)[:,:,5]>0).any(axis=1)


def candidate_scores(bank,arrays,checkpoint):
    checkpoint=Path(checkpoint)
    config=json.loads((checkpoint/'config.json').read_text())
    assert config['gate']=='any_explicit_arithmetic_mismatch'
    scores=baseline_scores(bank,arrays,checkpoint/'baseline')
    mask=gate_mask(bank)
    if mask.any():
        indices=np.flatnonzero(mask)
        selected_bank=[bank[int(i)] for i in indices]
        selected_arrays={'embeddings':arrays['embeddings'][indices]}
        scores[mask]=numeric_scores(selected_bank,selected_arrays,checkpoint/'numeric')
    return scores


def predict(bank,arrays,checkpoint):
    if not bank:
        return []
    return [int(i) for i in candidate_scores(bank,arrays,checkpoint).argmax(axis=1)]
