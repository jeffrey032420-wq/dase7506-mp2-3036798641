"""Finite grounding vs ancestry ablation, separate train-only and validation stages."""
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[k] = '4'
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import numpy as np
from threadpoolctl import threadpool_limits
from common import load_inputs,validate_choices
from train_round1 import labels
from train_round108_group_subsets import closure,digest,write,asset_inventory,metrics
from train_round109_arithmetic_residual import residual_scale,residual_design,fit_residual
from train_round110_residual_ablation import gradient_check
from train_round121_regularization import comparison
from evaluate_round108_group_subsets import fresh,expanded
from method_round108_group_subsets import tables
from method_round109_arithmetic_residual import read_anchor,anchored
from method_round110_residual_ablation import feature_tables as local_tables
from method_round120_question_interaction import question_hash,evidence_tables,add_interaction,candidate_scores as parent_scores
from method_round123_grounded_chain import COLUMNS,NAMES,feature_tables,candidate_scores,contracts

CODE = Path(__file__).resolve().parent
ROOT = CODE.parent
BASE = CODE/'runs/round108-group-subsets'
OLD = CODE/'runs/round110-residual-ablation'
PRIOR = CODE/'runs/round120-question-interaction'
PARENT = PRIOR/'candidates/round120_question_both'
AUDIT = CODE/'runs/round123-train-audit-v2'
OUT = CODE/'runs/round123-grounded-chain'
EVAL = CODE/'runs/round123-evaluation'
PLAN = ROOT/'ROUND123_GROUNDED_CHAIN_PLAN.md'
PENALTIES = (.1,.01)


def model_name(mode,p):
    return 'round123_'+mode+'_l'+str(p).replace('.','p')


def worker():
    tick = time.perf_counter();sources = closure(['train_round123_grounded_chain.py'])
    prior = json.loads((PRIOR/'result.json').read_text(encoding='utf-8'));audit = json.loads((AUDIT/'audit.json').read_text(encoding='utf-8'))
    assert all(digest(CODE/n)==sha for n,sha in prior['sources'].items())
    assert all(digest(CODE/n)==sha for n,sha in audit['sources'].items())
    assert digest(AUDIT/'candidate-features.npy')==audit['feature_sha256'] and not audit['validation_used'] and not audit['test_used']
    inherited = dict(prior['inherited'])
    paths = [PRIOR/'result.json',PRIOR/'round120_question_both-oof-scores.npy',AUDIT/'audit.json',AUDIT/'candidate-features.npy',
             *[PRIOR/f'fold{f}-question_both.npz' for f in range(3)],*[p for p in PARENT.rglob('*') if p.is_file()]]
    for p in paths:
        inherited[p.relative_to(CODE).as_posix()] = digest(p)
    assert all(digest(CODE/n)==sha for n,sha in inherited.items())
    parent_assets = asset_inventory(PARENT);plan_sha = digest(PLAN)
    (OUT/'sources').mkdir()
    for n in sources:
        shutil.copy2(CODE/n,OUT/'sources'/n)
    shutil.copy2(PLAN,OUT/'sources/PLAN.md')
    write(OUT/'pretraining.json',dict(sources=sources,inherited=inherited,parent_assets=parent_assets,plan_sha256=plan_sha,penalties=PENALTIES,modes=COLUMNS))
    bank,arrays = load_inputs('train');y = labels(bank,'train')
    data = tables(bank,arrays);local = local_tables(bank,data,'final_evidence');ev = evidence_tables(bank,data)
    q = np.stack([question_hash(r['question']) for r in bank]);cached = np.load(AUDIT/'candidate-features.npy')
    assert cached.shape==(len(bank),4,12)
    full = [[np.r_[cached[i,g['members']].mean(0),cached[i,g['members']].max(0)] for g in gs] for i,gs in enumerate(data)]
    features = {m:[[v[cols] for v in row] for row in full] for m,cols in COLUMNS.items()}
    for m in COLUMNS:
        live = feature_tables(bank[:13],data[:13],m)
        for actual,expected in zip(live,features[m][:13]):
            np.testing.assert_array_equal(actual,expected)
    folds = json.loads((BASE/'folds.json').read_text(encoding='utf-8'))
    parent_oof = np.load(PRIOR/'round120_question_both-oof-scores.npy');assert metrics(bank,y,parent_oof)['correct']==4396
    oof = {(m,p):np.zeros((len(bank),4)) for m in COLUMNS for p in PENALTIES};records,checks,configs,models = [],{},{},[];fits = 0
    for fr in folds:
        f = fr['fold'];fitting,held = np.asarray(fr['fit']),np.asarray(fr['held']);assert not set(fitting)&set(held)
        base = read_anchor(data,BASE/f'fold-models/fold{f}-round108_subsets_l0p01')
        with np.load(OLD/f'outer{f}-final_evidence.npz',allow_pickle=False) as z:
            base = anchored(data,local,base,z['mean'],z['scale'],z['weight'])
        with np.load(PRIOR/f'fold{f}-question_both.npz',allow_pickle=False) as z:
            base = add_interaction(data,ev,q,base,list(range(32)),z['mean'],z['scale'],z['weight'])
        np.testing.assert_allclose(base[held],parent_oof[held],rtol=1e-10,atol=1e-10)
        for mode,evidence in features.items():
            mean,scale = residual_scale(evidence,fitting);x,offset,importance,pair_audit = residual_design(data,evidence,y,fitting,scale,base)
            np.savez_compressed(OUT/f'fold{f}-{mode}-pair-audit.npz',**pair_audit)
            if mode not in checks:
                checks[mode] = gradient_check(x,offset,importance)
            for p in PENALTIES:
                weight,fit = fit_residual(x,offset,importance,p);fits += 1
                scores = anchored([data[i] for i in held],[evidence[i] for i in held],base[held],mean,scale,weight)
                oof[(mode,p)][held] = scores;np.savez(OUT/f'fold{f}-{model_name(mode,p)}.npz',mean=mean,scale=scale,weight=weight)
                records.append(dict(fold=f,mode=mode,lambda_value=p,fit=fit,held=metrics([bank[i] for i in held],y[held],scores),
                                    parent_held=metrics([bank[i] for i in held],y[held],base[held]),**comparison(y[held],base[held],scores)))
                write(OUT/'fit-progress.json',records);print('OUTER '+json.dumps(records[-1]),flush=True)
    configurations = []
    for mode in COLUMNS:
        for p in PENALTIES:
            scores = oof[(mode,p)];name = model_name(mode,p);np.save(OUT/(name+'-oof-scores.npy'),scores)
            configurations.append(dict(name=name,mode=mode,lambda_value=p,train_oof=metrics(bank,y,scores),**comparison(y,parent_oof,scores),
                                       fold_deltas_vs_parent=[r['held']['correct']-r['parent_held']['correct'] for r in records if r['mode']==mode and r['lambda_value']==p]))
    selected = [min([r for r in configurations if r['mode']==m],key=lambda r:(-r['train_oof']['correct'],-r['lambda_value'])) for m in COLUMNS]
    write(OUT/'selection-train-only.json',dict(candidates=selected,configurations=configurations,validation_used=False,test_used=False))
    base = parent_scores(bank,arrays,PARENT)
    for row in selected:
        mode,p = row['mode'],row['lambda_value'];evidence = features[mode]
        path = OUT/'candidates'/row['name'];path.mkdir(parents=True);shutil.copytree(PARENT,path/'parent')
        write(path/'config.json',dict(schema='grounded_chain_soft_residual_v1',mode=mode,lambda_value=p,fit_split='train',parent='round120_question_both',
                                      features=len(COLUMNS[mode]),margin_mode='same_fit_frozen_parent',constants=[0,1,2,7,10,12,24,60,100],source='bounded_input_only_graph'))
        mean,scale = residual_scale(evidence,np.arange(len(bank)));x,offset,importance,pair_audit = residual_design(data,evidence,y,np.arange(len(bank)),scale,base)
        weight,fit = fit_residual(x,offset,importance,p);fits += 1
        np.savez(path/'chain.npz',mean=mean,scale=scale,weight=weight);np.savez_compressed(OUT/f'{mode}-full-pair-audit.npz',**pair_audit)
        expected = anchored(data,evidence,base,mean,scale,weight)
        np.testing.assert_array_equal(anchored(data,evidence,base,mean,scale,np.zeros(len(weight))),base)
        np.testing.assert_allclose(candidate_scores(bank[:53],{'embeddings':arrays['embeddings'][:53]},path),expected[:53],rtol=1e-10,atol=1e-10)
        export_checks = contracts(bank[:53],{'embeddings':arrays['embeddings'][:53]},path)
        export_checks.update(zero_correction_exact_parent=True,export_agrees=True,parent_outer_held_scores_reproduced=True,pure_input_cache_agrees=True)
        model = dict(**row,method='method_round123_grounded_chain.py',checkpoint=path.relative_to(CODE).as_posix(),
                     train_resubstitution_not_oof=metrics(bank,y,expected),fit=fit,checks=export_checks,assets=asset_inventory(path))
        models.append(model);print('EXPORT '+json.dumps({k:v for k,v in model.items() if k not in ('checks','assets')}),flush=True)
    assert fits==21 and closure(['train_round123_grounded_chain.py'])==sources and digest(PLAN)==plan_sha
    assert asset_inventory(PARENT)==parent_assets and all(digest(CODE/n)==sha for n,sha in inherited.items())
    write(OUT/'result.json',dict(status='completed_train_only',models=models,configurations=configurations,fold_records=records,sources=sources,inherited=inherited,
                                plan_sha256=plan_sha,parent_assets=parent_assets,model_fits=fits,mathematical_checks=checks,seconds=time.perf_counter()-tick,
                                threads_total=4,validation_used=False,test_used=False))
    print('TRAIN_COMPLETE '+json.dumps(dict(fits=fits,seconds=time.perf_counter()-tick,selected=selected)),flush=True)


def evaluate():
    assert not EVAL.exists();trained = json.loads((OUT/'result.json').read_text(encoding='utf-8'))
    assert trained['model_fits']==21 and not trained['validation_used'] and not trained['test_used']
    assert all(digest(CODE/n)==s for n,s in trained['sources'].items()) and digest(PLAN)==trained['plan_sha256']
    assert all(digest(CODE/n)==s for n,s in trained['inherited'].items())
    ppath,cpath = ROOT/'CURRENT_BEST.json',ROOT/'RESEARCH_CANDIDATE_ROUND120.json'
    pbytes,cbytes = ppath.read_bytes(),cpath.read_bytes();pointer = json.loads(pbytes)
    assert pointer['research_best_candidate']==cpath.name and pointer['research_best_validation_correct']==752 and pointer['round']==79
    final_assets = asset_inventory(ROOT/pointer['checkpoint'])
    prior = json.loads((PRIOR/'result.json').read_text(encoding='utf-8'))
    control = dict(next(r for r in prior['models'] if r['name']=='round120_question_both'),lambda_value=.1,is_previous_research_control=True,fold_deltas_vs_parent=[-1,1,-2])
    models = [control,*trained['models']];sources = closure(['train_round123_grounded_chain.py'])
    manifest = json.loads((CODE/'PACKAGE_MANIFEST.json').read_text(encoding='utf-8'))['files']
    for n in ('common.py','predict.py','score_predictions.py','check_data.py'):
        assert digest(CODE/n)==manifest['code/'+n]
    for r in models:
        assert asset_inventory(CODE/r['checkpoint'])==r['assets'] and all(r['checks'].values()) and expanded(CODE/r['checkpoint'])<=16*2**20
    selection_train = json.loads((OUT/'selection-train-only.json').read_text(encoding='utf-8'))
    assert [r['name'] for r in selection_train['candidates']]==[r['name'] for r in trained['models']]
    EVAL.mkdir();(EVAL/'sources').mkdir()
    for n in sources:
        shutil.copy2(CODE/n,EVAL/'sources'/n)
    shutil.copy2(PLAN,EVAL/'sources/PLAN.md');(EVAL/'current-pointer-before.json').write_bytes(pbytes)
    frozen = dict(models=models,sources=sources,plan_sha256=digest(PLAN),training_result_sha256=digest(OUT/'result.json'),train_selection_sha256=digest(OUT/'selection-train-only.json'),
                  selection_rule='max validation, then train OOF, then smaller assets and name',test_score_used=False,final79_assets=final_assets)
    write(EVAL/'frozen-before-validation.json',frozen)
    bank,arrays = load_inputs('validation');y = labels(bank,'validation');base = parent_scores(bank,arrays,PARENT)
    right_base = y[np.arange(len(y)),base.argmax(1)].astype(bool);assert right_base.sum()==752
    results = []
    for row in models:
        is_control = row.get('is_previous_research_control',False);path = CODE/row['checkpoint']
        scores = parent_scores(bank,arrays,path) if is_control else candidate_scores(bank,arrays,path)
        choices = [int(j) for j in scores.argmax(1)];validate_choices(bank,[r['id'] for r in bank],choices)
        audit = fresh(row['method'],path,EVAL/row['name']);local = metrics(bank,y,scores)
        assert audit['official_score']['correct']==local['correct']
        assert json.loads((EVAL/row['name']/'validation-predictions.json').read_text(encoding='utf-8'))['selected']==choices
        right = y[np.arange(len(y)),choices].astype(bool)
        checked = row['checks'] if is_control else contracts(bank[:53],{'embeddings':arrays['embeddings'][:53]},path)
        result = dict(name=row['name'],method='code/'+row['method'],checkpoint='code/'+row['checkpoint'],mode=row['mode'],lambda_value=row['lambda_value'],**local,
                      train_oof=row['train_oof'],train_resubstitution_not_oof=row['train_resubstitution_not_oof'],fold_deltas_vs_parent=row['fold_deltas_vs_parent'],
                      is_previous_research_control=is_control,fixed_current752_errors=int((~right_base&right).sum()),new_current752_errors=int((right_base&~right).sum()),
                      changed_validation_choices=int((np.array(choices)!=base.argmax(1)).sum()),checks=checked,uncompressed_asset_bytes=expanded(path),**audit,
                      status='verified_local_validation',reference_cpu_complete_test_verified=False)
        results.append(result);write(EVAL/'all-results.json',results);print('VALIDATION '+json.dumps(result),flush=True)
    assert ppath.read_bytes()==pbytes and cpath.read_bytes()==cbytes and closure(['train_round123_grounded_chain.py'])==sources
    assert all(digest(CODE/n)==s for n,s in trained['inherited'].items()) and all(asset_inventory(CODE/r['checkpoint'])==r['assets'] for r in models)
    assert digest(PLAN)==frozen['plan_sha256'] and digest(OUT/'result.json')==frozen['training_result_sha256']
    assert digest(OUT/'selection-train-only.json')==frozen['train_selection_sha256'] and asset_inventory(ROOT/pointer['checkpoint'])==final_assets
    best = min(results,key=lambda r:(-r['correct'],-r['train_oof']['correct'],r['uncompressed_asset_bytes'],r['name']))
    chosen = best if not best['is_previous_research_control'] else None
    selection = dict(status='new_candidate_selected_before_test' if chosen else 'retain_previous_research_candidate',candidate=chosen['name'] if chosen else None,
                     metrics=chosen,development_best=best,selection_splits=['train_oof','validation'],test_score_used=False,max_new_test_candidates=1,
                     user_conditionally_authorized_test=True,plan_sha256=digest(PLAN),frozen_manifest_sha256=digest(EVAL/'frozen-before-validation.json'))
    write(EVAL/'selection-before-test.json',selection)
    write(EVAL/'integrity.json',dict(status='passed',source_and_assets_unchanged=True,current120_preserved=True,final79_preserved=True,test_used_for_training_or_selection=False))
    if chosen:
        write(ROOT/'RESEARCH_CANDIDATE_ROUND123.json',{**chosen,'new_test_score':None,'selection_evidence':selection,'prior_test_aggregates_known':True,'final_submission_model_not_changed':True})
        pointer.update(research_best_candidate='RESEARCH_CANDIDATE_ROUND123.json',research_best_validation_correct=best['correct'],
                       research_selection_reason='Predeclared validation/OOF/assets ordering; before new test',research_selection_record='code/runs/round123-evaluation/selection-before-test.json',
                       research_candidate_test_score=None,research_candidate_test_correct=None,research_candidate_test_n=None,research_candidate_test_accuracy=None)
    lines = ['# Round123：数字来源与最终计算链消融','','## Material Passport','',
             'academic-research-suite / experiment-agent；2026-10-29；VERIFIED_LOCAL_VALIDATION。21新拟合，4最终输出官方验证。','',
             '## 假设与输入审计','',
             '12/14等历史已有正确链/数量覆盖，本轮区分最终祖先中的真假运算并学习软修正。仅按训练信息设计和选择。'
             'grounding/ancestry/both对359训练错的差异覆盖300/256/308题；覆盖不是可修复数。最终祖先可见算术错的161候选中149错误，'
             '但父错仅1题选到此类候选，剩余简单算术空间很小。放宽来源的完整真链3904候选仍有752错误，因此不以真链证明题意正确。','',
             '|特征|λ|训练OOF/4755|修复父错/新增错|三折净变化|选中|','|---|---:|---:|---|---|---|']
    chosen_names = {r['name'] for r in trained['models']}
    for r in trained['configurations']:
        lines.append(f'|{r["mode"]}|{r["lambda_value"]}|{r["train_oof"]["correct"]}|{r["fixed_parent_errors"]}/{r["new_parent_errors"]}|{r["fold_deltas_vs_parent"]}|{r["name"] in chosen_names}|')
    lines += ['', '|最终候选|训练OOF|回代|验证/798|分歧/355|单正确/117|修复752错/新增错|KiB|fresh秒|',
              '|---|---:|---:|---:|---:|---:|---|---:|---:|']
    for r in results:
        lines.append(f'|{r["name"]}|{r["train_oof"]["correct"]}|{r["train_resubstitution_not_oof"]["correct"]}|{r["correct"]}|{r["disagreement_correct"]}|{r["single_correct"]}|{r["fixed_current752_errors"]}/{r["new_current752_errors"]}|{r["uncompressed_asset_bytes"]/1024:.2f}|{r["prediction_plus_scoring_wall_seconds"]:.3f}|')
    lines += ['',f'开发选择：{best["name"]}，验证{best["correct"]}/798。'+('新候选按计划选出，须一次独立冻结test。' if chosen else '保留原120，未新增test。'),'',
              '## 核验与局限','',f'18outer+3full=21拟合，worker{trained["seconds"]:.3f}秒，总4线程，600秒硬限。父held分数1e-10复现，纯输入缓存/梯度/重复pair/每题权重/fit-only scaler/收敛/导出/零修正/重排等接口通过。全部资产≤16MiB；fresh validation预测+独立评分≤30秒，参考Xeon未验证。', '',
              '首次自检在数据/训练前发现通用常数遮蔽前序运算，已修正优先级，失败及原源码保留，完成审计输出新v2目录。'
              'same-fit frozen parent offset并非inner-OOF。数值相同不能确定实体，部分公式/文字未知；完整算术真链不能验证题意。'
              '六训练配置和四最终验证输出全部保留，未按验证追加网格。长期自适应train/validation及已知历史测试汇总如实披露，未用新test调参或分析个题。','',
              '## 统计解释检查11/11','',
              '1 Simpson：分歧/单正确及三折同时报告。2 Ecological：只对该固定题库作描述。3 Berkson：候选集筛选分布限制外推。'
              '4 Collider：不以条件子集作因果推断。5 Base rate：信号同时报告正确/错误计数和分母。6 Regression to mean：小变动与开发选择不称稳定收益。'
              '7 Survivorship：六训练配置含失败全部保留。8 Look-elsewhere：披露有限搜索和历史多次比较，不报显著。9 Forking paths：计划冻结、参数先按OOF选择。'
              '10 Correlation/causation与11 Reverse causality：不作因果方向主张。','',
              '复现：code目录audit_round123_grounded_chain.py、train_round123_grounded_chain.py，然后训练脚本--evaluate；原输出拒绝覆盖。证据runs/round123-train-audit（首次失败）、round123-train-audit-v2、round123-grounded-chain、round123-evaluation。','']
    report = '\n'.join(lines);(ROOT/'ROUND123_RESULTS.md').write_text(report,encoding='utf-8')
    with (ROOT/'WORKLOG.md').open('a',encoding='utf-8') as f:
        f.write('\n\n'+report)
    with (ROOT/'AI_DISCLOSURE.md').open('a',encoding='utf-8') as f:
        f.write('\n\n## 2026-10-29 — Round123 grounded final-chain soft features\n\nCodex audited input-only numerical grounding and false-equation ancestry, preserving an initial pre-data fixture failure and its fix. It predeclared3 feature families x2 penalties,21 fits, train-OOF lambda selection and4 final official validations. All outcomes, source/assets, resource/interface checks and interpretation limits are recorded. No test guided training/selection; adaptive development and prior test aggregates disclosed.\n')
    pointer.update(latest_completed_development_round=123,latest_round_result=f'Round123 grounded-chain max {best["correct"]}/798; '+('new candidate selected before test' if chosen else 'retain120, no new test')+'. See ROUND123_RESULTS.md.')
    write(ppath,pointer);write(EVAL/'completion.json',dict(status='completed_validation',new_fits=21,official_final_outputs=4,best_validation_correct=best['correct'],selected_for_frozen_test=chosen['name'] if chosen else None,test_executed_in_this_script=False))
    print('ROUND123_COMPLETE '+json.dumps(dict(best=best['name'],validation=best['correct'],new_test_admitted=bool(chosen))),flush=True)


def main():
    if '--evaluate' in sys.argv:
        with threadpool_limits(limits=4):
            evaluate()
        return
    if '--worker' in sys.argv:
        with threadpool_limits(limits=4):
            worker()
        return
    assert not OUT.exists(),'Preserve original evidence';OUT.mkdir(parents=True);tick = time.perf_counter()
    try:
        p = subprocess.run([sys.executable,'-X','utf8',str(Path(__file__).resolve()),'--worker'],cwd=CODE,timeout=600)
        write(OUT/'process-monitor.json',dict(exit_code=p.returncode,wall_seconds=time.perf_counter()-tick,hard_timeout_seconds=600));assert p.returncode==0
    except subprocess.TimeoutExpired:
        write(OUT/'process-monitor.json',dict(status='hard_timeout',wall_seconds=time.perf_counter()-tick));raise


if __name__=='__main__':
    main()
