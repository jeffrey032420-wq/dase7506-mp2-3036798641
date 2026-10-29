"""Deterministic candidate features: no references, IDs or fitted state."""
import re
import numpy as np
from common import parse_answer

TEXT_NAMES = ['log_chars', 'log_words', 'log_lines', 'log_numbers',
              'log_equals', 'log_question_chars', 'has_answer', 'agreement',
              'distinct_answers', 'has_box', 'has_hash', 'uncertainty',
              'relative_log_chars', 'relative_log_words']


def answer_groups(bank):
    return [[parse_answer(c['text']) for c in r['candidates']] for r in bank]


def majority_choices(bank):
    # Unparseable answers never form an agreement group. Ties: first candidate.
    return [int(np.argmax([a.count(v) if v is not None else 0 for v in a]))
            for a in answer_groups(bank)]


def build_features(bank, arrays, mode):
    emb = np.asarray(arrays['embeddings'], dtype=np.float64)
    if mode == 'embeddings':
        return emb.reshape(-1, emb.shape[-1])
    rows = []
    for row, answers in zip(bank, answer_groups(bank)):
        group = []
        for c, answer in zip(row['candidates'], answers):
            t = c['text']
            group.append([np.log1p(len(t)), np.log1p(len(t.split())),
                          np.log1p(t.count('\n')), np.log1p(len(re.findall(r'\d+', t))),
                          np.log1p(t.count('=')), np.log1p(len(row['question'])),
                          float(answer is not None), answers.count(answer)/4 if answer is not None else 0,
                          len(set(a for a in answers if a is not None))/4,
                          float('\\boxed' in t), float('####' in t),
                          float(bool(re.search(r'\b(maybe|perhaps|unsure|not sure)\b', t.lower())))])
        g = np.asarray(group)
        rows.append(np.column_stack([g, g[:, :2] - g[:, :2].mean(axis=0)]))
    text = np.asarray(rows).reshape(-1, len(TEXT_NAMES))
    if mode == 'text':
        return text
    if mode == 'combined':
        return np.column_stack([emb.reshape(-1, emb.shape[-1]), text])
    raise ValueError(f'Unknown feature mode: {mode}')
