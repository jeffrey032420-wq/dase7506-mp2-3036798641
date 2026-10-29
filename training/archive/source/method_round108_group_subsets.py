"""Numeric-answer group linear selector; only supplied inputs and explicit assets."""
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import re
import numpy as np
from common import parse_answer

BOUND = 10**12
TOKEN = re.compile(r'(?<![\w.,/])[-+]?(?:\d[\d,]*(?:\.\d+)?|\.\d+)(?:/[-+]?(?:\d+(?:\.\d+)?|\.\d+))?(?![\w,/]|\.\d)')
LITERAL = re.compile(r'[-+]?(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?|[-+]?\.\d+')


def question_numbers(question):
    values = []
    for match in TOKEN.finditer(question[:20000]):
        token = match.group().rstrip(',')
        if len(token) > 80:
            continue
        parts = token.split('/')
        if not all(LITERAL.fullmatch(x) for x in parts):
            continue
        try:
            v = Fraction(parts[0].replace(',', ''))
            if len(parts) == 2:
                v /= Fraction(parts[1].replace(',', ''))
            if abs(v) <= BOUND and v.denominator <= BOUND:
                values.append(v)
        except (ValueError, ZeroDivisionError):
            continue
        if len(values) == 16:
            break
    return values


def numeric_surface(answer, numbers):
    a = Fraction(answer)
    magnitude = float(min(abs(a), BOUND))
    maximum = max((abs(v) for v in numbers), default=Fraction(0))
    divisor = max(float(maximum), 1/BOUND) if maximum else 1.
    return np.array([float((a > 0)-(a < 0)), np.log1p(magnitude), float(a.denominator == 1),
                     float(a in numbers), np.log1p(len(numbers)), np.log1p(magnitude/divisor)])


def representation(embedding, support, group_count, surface):
    mean = embedding.mean(0)
    return np.r_[mean, support, support/4, group_count, np.square(embedding-mean).mean(), surface]


def tables(bank, arrays, include_subsets=False):
    embeddings = np.asarray(arrays['embeddings'], dtype=np.float64)
    assert embeddings.shape == (len(bank), 4, 1024) and np.isfinite(embeddings).all()
    result = []
    for i, row in enumerate(bank):
        grouped = {}
        for j, candidate in enumerate(row['candidates']):
            answer = parse_answer(candidate['text'])
            if answer is not None:
                grouped.setdefault(answer, []).append(j)
        q = []
        numbers = question_numbers(row['question'])
        for answer in sorted(grouped):
            members = sorted(grouped[answer], key=lambda j: (row['candidates'][j]['text'], embeddings[i, j].tobytes()))
            surface = numeric_surface(answer, numbers)
            full = representation(embeddings[i, members], len(members), len(grouped), surface)
            variants, masks = [], []
            if include_subsets:
                for size in range(1, len(members)+1):
                    for selected in combinations(members, size):
                        variants.append(representation(embeddings[i, list(selected)], size, len(grouped), surface))
                        masks.append(sum(1 << j for j in selected))
            else:
                variants.append(full)
                masks.append(sum(1 << j for j in members))
            assert full.shape == (1034,) and np.isfinite(full).all()
            q.append({'members': members, 'full': full, 'variants': np.asarray(variants), 'masks': masks})
        result.append(q)
    return result


def score_tables(data, mean, scale, weight):
    result = np.full((len(data), 4), -1e100)
    for i, groups in enumerate(data):
        if not groups:
            result[i] = 0.
        for group in groups:
            value = ((group['full']-mean)/scale)@weight
            result[i, group['members']] = value
    assert np.isfinite(result).all()
    return result


def candidate_scores(bank, arrays, checkpoint):
    if not bank:
        return np.empty((0, 4))
    checkpoint = Path(checkpoint)
    cfg = json.loads((checkpoint/'config.json').read_text(encoding='utf-8'))
    assert cfg['schema'] == 'numeric_answer_group_1034_v1'
    with np.load(checkpoint/'weights.npz', allow_pickle=False) as z:
        return score_tables(tables(bank, arrays), z['mean'], z['scale'], z['weight'])


def predict(bank, arrays, checkpoint):
    return [int(j) for j in candidate_scores(bank, arrays, checkpoint).argmax(1)] if bank else []
