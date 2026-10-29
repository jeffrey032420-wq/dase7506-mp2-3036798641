"""Route explicit final-answer evidence to candidates scored as that answer."""
import json
import re
from pathlib import Path
from fractions import Fraction
import numpy as np
from common import parse_answer
from method_round7_gated import candidate_scores as incumbent_scores

NUMBER=re.compile(r'[-+]?\d[\d,]*(?:\.\d+)?(?:/\d+)?')
BOX=re.compile(r'\\boxed\{([^{}]+)\}')


def final_box(text):
    boxes=list(BOX.finditer(text))
    if not boxes or '####' not in text or boxes[-1].start()<text.rfind('####'):
        return None
    m=NUMBER.search(boxes[-1].group(1))
    if not m: return None
    try: return str(Fraction(m.group().replace(',','')))
    except (ValueError,ZeroDivisionError): return None


def evidence(bank):
    official=[[parse_answer(c['text']) for c in r['candidates']] for r in bank]
    final=[[final_box(c['text']) for c in r['candidates']] for r in bank]
    mismatch=np.array([[v is not None and v!=a for a,v in zip(aa,vv)] for aa,vv in zip(official,final)])
    return official,final,mismatch


def adjust(bank,scores,config):
    official,final,bad=evidence(bank)
    out=scores.copy(); mode=config['mode']; strength=config.get('strength',1.)
    if mode=='penalty':
        scale=np.maximum(scores.std(axis=1,keepdims=True),1e-10)
        return scores-strength*scale*bad
    for n,(a,v) in enumerate(zip(official,final)):
        if mode in ('transfer','clean_transfer'):
            j=int(scores[n].argmax())
            if not bad[n,j]: continue
            accept=np.array([x==v[j] and (mode!='clean_transfer' or not bad[n,i]) for i,x in enumerate(a)])
            if accept.any():
                out[n,accept]+=np.ptp(scores[n])+1
        elif mode=='vote':
            for j in range(4):
                if not bad[n,j]: continue
                accept=np.array([x==v[j] and not bad[n,i] for i,x in enumerate(a)])
                if accept.any():
                    target=np.maximum(out[n,accept],scores[n,j])
                    out[n,accept]=(1-strength)*out[n,accept]+strength*target
    return out


def candidate_scores(bank,arrays,checkpoint):
    checkpoint=Path(checkpoint)
    config=json.loads((checkpoint/'config.json').read_text())
    return adjust(bank,incumbent_scores(bank,arrays,checkpoint/'incumbent'),config)


def predict(bank,arrays,checkpoint):
    if not bank: return []
    return [int(i) for i in candidate_scores(bank,arrays,checkpoint).argmax(axis=1)]
