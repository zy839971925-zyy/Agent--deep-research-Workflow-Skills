from __future__ import annotations

def validate_learning_semantics(r):
    fs=[]; status=r.get('status'); tier=r.get('tier'); prov=r.get('provenance') or {}
    if prov.get('intrinsic_reflection_only') and status in ('validated','promoted'):
        fs.append({'severity':'ERROR','code':'INTRINSIC_REFLECTION_NOT_VALIDATION','message':'same-model intrinsic reflection may create candidate insight only'})
    if tier==2 and status=='promoted' and not r.get('held_out_eval_refs'):
        fs.append({'severity':'ERROR','code':'ROUTING_LEARNING_NEEDS_HELDOUT_EVAL','message':'Tier 2 promotion requires held-out eval'})
    if tier==3 and status=='promoted':
        for field in ('regression_refs','held_out_eval_refs','baseline_comparison_ref','dual_review_ref','rollback_ref'):
            if not r.get(field): fs.append({'severity':'ERROR','code':'CANONICAL_PROMOTION_GATE','message':f'Tier 3 promotion requires {field}'})
    return fs

def retrievable(r,task_tags,gap_tags):
    if validate_learning_semantics(r): return False
    if r.get('status') not in ('validated','promoted'): return False
    if r.get('status') in ('stale','deprecated'): return False
    tags=set(task_tags)|set(gap_tags); sig=set(r.get('task_signature',[])); app=set(r.get('applicability_conditions',[])); anti=set(r.get('anti_conditions',[]))
    if anti & tags:return False
    return bool((sig|app)&tags)

def retrieve(records,task_tags,gap_tags,limit=3):
    c=[r for r in records if retrievable(r,task_tags,gap_tags)]
    c.sort(key=lambda r:(-(r.get('usage') or {}).get('helped',0), (r.get('usage') or {}).get('harmed',0),r.get('learning_id','')))
    return c[:max(0,min(limit,5))]
