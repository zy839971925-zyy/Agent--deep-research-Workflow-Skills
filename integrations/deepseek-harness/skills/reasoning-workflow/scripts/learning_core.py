from __future__ import annotations

def validate_learning_semantics(r):
    fs=[]; status=r.get('status'); tier=r.get('tier'); prov=r.get('provenance') or {}
    types=set(prov.get('feedback_types') or [])
    intrinsic=not (types-{'intrinsic_reflection'})
    if (prov.get('intrinsic_reflection_only') or intrinsic) and status in ('validated','promoted'):
        fs.append({'severity':'ERROR','code':'INTRINSIC_REFLECTION_NOT_VALIDATION','message':'same-model intrinsic reflection may create candidate insight only'})
    if status in ('validated','promoted') and not (r.get('validation_evidence_refs') or r.get('source_eval_refs') or r.get('eval_refs')):
        fs.append({'severity':'ERROR','code':'VALIDATION_EVIDENCE_REQUIRED','message':'validated/promoted requires resolvable validation evidence references; host resolves them'})
    if tier==2 and status=='promoted' and not r.get('held_out_eval_refs'):
        fs.append({'severity':'ERROR','code':'ROUTING_LEARNING_NEEDS_HELDOUT_EVAL','message':'Tier 2 promotion requires held-out eval'})
    if tier==3 and status=='promoted':
        for field in ('regression_refs','held_out_eval_refs','baseline_comparison_ref','dual_review_ref','rollback_ref'):
            if not r.get(field): fs.append({'severity':'ERROR','code':'CANONICAL_PROMOTION_GATE','message':f'Tier 3 promotion requires {field}'})
    return fs

def retrievable(r,task_tags,gap_tags,validation_resolver=None):
    from runtime_core import validate_schema
    from pathlib import Path
    if validate_schema(r,Path(__file__).resolve().parents[1]/'schemas/learning-record.schema.json') or validate_learning_semantics(r): return False
    if validation_findings(r,validation_resolver): return False
    if r.get('status') not in ('validated','promoted'): return False
    if r.get('status') in ('stale','deprecated'): return False
    tags=set(task_tags)|set(gap_tags); sig=set(r.get('task_signature',[])); app=set(r.get('applicability_conditions',[])); anti=set(r.get('anti_conditions',[]))
    if anti & tags:return False
    return bool((sig|app)&tags)

def retrieve(records,task_tags,gap_tags,limit=3,maintenance=False,validation_resolver=None):
    c=[r for r in records if (maintenance or r.get('tier')==1) and retrievable(r,task_tags,gap_tags,validation_resolver)]
    c.sort(key=lambda r:(-(r.get('usage') or {}).get('helped',0), (r.get('usage') or {}).get('harmed',0),r.get('learning_id','')))
    return c[:max(0,min(limit,5))]


def validation_findings(record,resolver=None):
    if record.get('status') not in ('validated','promoted'):return []
    refs=record.get('validation_evidence_refs') or record.get('source_eval_refs') or record.get('eval_refs') or []
    try: verified=bool(refs) and callable(resolver) and all(resolver(ref) is True for ref in refs)
    except Exception:verified=False
    findings=[] if verified else [{'severity':'ERROR','code':'LEARNING_VALIDATION_UNVERIFIED','message':'validated credit requires trusted validation evidence resolver; record labels alone are insufficient'}]
    gates={}
    if record.get('status')=='promoted' and record.get('tier') in (2,3): gates['held_out_eval_refs']='held_out'
    if record.get('status')=='promoted' and record.get('tier')==3:
        gates.update(regression_refs='regression',baseline_comparison_ref='baseline',dual_review_ref='dual_review',rollback_ref='rollback')
    for field,role in gates.items():
        values=record.get(field) or []
        values=values if isinstance(values,list) else [values]
        try:
            valid=bool(values) and callable(resolver) and all(resolver(ref,role=role,record=record) is True for ref in values)
        except Exception: valid=False
        if not valid: findings.append({'severity':'ERROR','code':'LEARNING_PROMOTION_EVIDENCE_UNVERIFIED','message':field+' requires typed, applicable, passing host evidence, not a nonempty reference'})
    return findings


def admit_record(record,root,validation_resolver=None):
    from runtime_core import validate_schema
    fs=[f.as_dict() for f in validate_schema(record,root/'schemas/learning-record.schema.json')]
    if fs:return fs
    return validate_learning_semantics(record)+validation_findings(record,validation_resolver)


def learning_subject_fingerprint(record):
    """Bind promotion evidence to the proposed lesson, not status/usage/ref bookkeeping."""
    import hashlib,json
    fields=('learning_id','tier','task_signature','failure_mode','root_cause_class','lesson_type',
        'heuristic','applicability_conditions','anti_conditions','proposed_patch_refs')
    payload={k:record[k] for k in fields if k in record}
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()

def file_evidence_resolver(index_path):
    """Offline trusted-host evidence index. Byte identity is not semantic truth.
    Index must be curated by the host, never supplied by a proposing worker.
    """
    import json,hashlib
    from pathlib import Path
    if index_path is None:return None
    path=Path(index_path).resolve();data=json.loads(path.read_text());base=path.parent
    if not isinstance(data,dict):raise ValueError('validation evidence index must be an object')
    def verify(ref,role=None,record=None):
        entry=data.get(ref,{})
        if not isinstance(entry,dict) or entry.get('verdict')!='pass':return False
        kinds={'external_evaluation','human_feedback','deterministic_test','external_observation'}
        if role is not None:
            kinds={'regression':{'deterministic_test'},'held_out':{'external_evaluation','deterministic_test'},
                'baseline':{'baseline_comparison'},'dual_review':{'independent_review'},'rollback':{'rollback_plan'}}.get(role,set())
            if (not record or role not in entry.get('roles',[]) or record.get('learning_id') not in entry.get('learning_ids',[]) or
                entry.get('current') is not True or entry.get('subject_sha256') != learning_subject_fingerprint(record)):return False
            if role=='dual_review' and entry.get('independence_verified') is not True:return False
        if entry.get('kind') not in kinds:return False
        try:
            p=(base/entry['path']).resolve();p.relative_to(base)
            return hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256']
        except (OSError,ValueError,KeyError,TypeError):return False
    return verify
