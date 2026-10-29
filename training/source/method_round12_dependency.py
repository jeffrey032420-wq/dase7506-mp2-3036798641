"""Backward coverage through strict, correct numerical equalities."""
import ast
import json
import re
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import numpy as np
from common import parse_answer
from numeric_round7_v3 import normalize, evaluate
from method_round11 import candidate_scores as incumbent_scores

NUMBER = re.compile(r'[-+]?\d[\d,]*(?:\.\d+)?(?:/\d+)?(?:\s*%)?')


def question_values(question):
    values = set()
    for match in NUMBER.finditer(question):
        text = match.group().replace(',', '').replace(' ', '')
        try:
            values.add(Fraction(text.rstrip('%')) / (100 if text.endswith('%') else 1))
        except (ValueError, ZeroDivisionError):
            pass
    return values


def operand_values(expression):
    expression = expression.strip()
    tree = ast.parse(expression, mode='eval')
    if not isinstance(tree.body, ast.BinOp):
        return None
    values = set()
    def walk(node):
        if isinstance(node, ast.Constant):
            values.add(Fraction(ast.get_source_segment(expression, node)))
        elif isinstance(node, ast.UnaryOp) and isinstance(node.operand, ast.Constant):
            values.add(evaluate(ast.get_source_segment(expression, node)))
        else:
            for child in ast.iter_child_nodes(node):
                walk(child)
    walk(tree.body)
    return values


def graph_records(text):
    normalized = normalize(text)
    records = []
    for match in re.finditer(r'[0-9(+\-][0-9.()+*/\-= \t]*', normalized):
        run = match.group()
        if '=' not in run:
            continue
        parts = run.split('=')
        prefix, suffix = normalized[:match.start()], normalized[match.end():]
        previous = prefix.rsplit('\n', 1)[-1].rstrip()
        unsafe_left = bool(prefix and (prefix[-1].isalnum() or prefix[-1] in '^_\\'))
        unsafe_left |= bool(previous and (previous[-1].isalnum() or previous[-1] in '*/^_\\|)]}'))
        unsafe_right = bool(suffix and (suffix[0].isalnum() or suffix[0] in '^_\\'))
        for i, (a, b) in enumerate(zip(parts, parts[1:])):
            if i == 0 and unsafe_left or i == len(parts)-2 and unsafe_right:
                continue
            try:
                left, right = evaluate(a), evaluate(b.strip().rstrip('.'))
                operands = operand_values(a)
                # Right side must state a scalar result, not another expression.
                if operands is None or not re.fullmatch(r'\s*[-+]?\d+(?:\.\d+)?\.?\s*', b) or left != right:
                    continue
                records.append((right, operands))
            except (ValueError, SyntaxError, ZeroDivisionError, OverflowError, RecursionError):
                continue
            if len(records) >= 64:
                return records
    return records


def candidate_coverage(question_numbers, text):
    parsed = parse_answer(text)
    if parsed is None:
        return {'known': False, 'covered': [], 'missing': [], 'nodes': 0}
    final = Fraction(parsed)
    records = graph_records(text)
    @lru_cache(None)
    def trace(value, before):
        covered = {value} & question_numbers
        used = set()
        for i, (output, operands) in enumerate(records[:before]):
            if output != value:
                continue
            used.add(i)
            for operand in operands:
                sub_covered, sub_used = trace(operand, i)
                covered.update(sub_covered)
                used.update(sub_used)
        return frozenset(covered), frozenset(used)
    covered, used = trace(final, len(records))
    missing = question_numbers - covered
    return {'known': len(question_numbers) >= 3 and len(used) >= 2,
            'covered': sorted(map(str, covered)), 'missing': sorted(map(str, missing)), 'nodes': len(used)}


def evidence(bank):
    features, diagnostics = [], []
    for row in bank:
        inputs = question_values(row['question'])
        candidates = [candidate_coverage(inputs, c['text']) for c in row['candidates']]
        complete_exists = any(c['known'] and not c['missing'] for c in candidates)
        features.append([len(c['missing']) / max(len(inputs), 1) if complete_exists and c['known'] else 0
                         for c in candidates])
        diagnostics.append({'question_inputs': sorted(map(str, inputs)), 'candidates': candidates})
    return np.asarray(features, dtype=np.float64), diagnostics


def adjust(scores, features, config):
    scale = np.maximum(scores.std(axis=1, keepdims=True), 1e-10)
    return scores - config['strength'] * scale * features


def candidate_scores(bank, arrays, checkpoint):
    checkpoint = Path(checkpoint)
    config = json.loads((checkpoint / 'config.json').read_text())
    features, _ = evidence(bank)
    return adjust(incumbent_scores(bank, arrays, checkpoint / 'incumbent'), features, config)


def predict(bank, arrays, checkpoint):
    if not bank:
        return []
    return [int(i) for i in candidate_scores(bank, arrays, checkpoint).argmax(axis=1)]
