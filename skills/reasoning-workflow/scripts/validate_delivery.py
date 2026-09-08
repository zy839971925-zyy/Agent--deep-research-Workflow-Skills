#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from semantic_core import load_json, validate_schema, finding
from validate_state import validate as validate_state

REQ_MAP={'satisfied':'satisfied','not_applicable':'not_applicable','deferred':'deferred','blocked':'blocked','superseded':'superseded'}

def validate(state,manifest,root=None):
    skill_root=Path(__file__).resolve().parents[1]
    findings=validate_schema(manifest,skill_root/'schemas/delivery-manifest.schema.json')
    state_findings,registry,closure=validate_state(state,skill_root)
    # include state semantic errors because readiness cannot outrun canonical state
    findings += [f for f in state_findings if f.severity=='ERROR']
    if not isinstance(state,dict) or not isinstance(manifest,dict):
        return findings,{'computed_delivery_ready':False,'epistemic_closure':closure}
    for layer,key in (('epistemic','computed_epistemic_closed'),('runtime','computed_runtime_closed')):
        result=closure[layer]
        if result.get('applicable') and not result[key]:
            findings.append(finding('ERROR','DELIVERY_CLOSURE_BLOCKED',f'{layer} closure is unresolved: {result["blockers"]}'))
    for collection in ('requirements','acceptance_criteria','artifacts'):
        rows=manifest.get(collection,[])
        if not isinstance(rows,list) or any(not isinstance(x,dict) for x in rows):
            return findings,{'computed_delivery_ready':False,'epistemic_closure':closure}
        ids=[x.get('id') for x in rows]
        if len(ids)!=len(set(ids)):
            findings.append(finding('ERROR','DELIVERY_DUPLICATE_ID',f'duplicate id in {collection}'))
    if manifest.get('work_id')!=state.get('work_id'): findings.append(finding('ERROR','WORK_ID_MISMATCH','manifest.work_id does not match state.work_id'))
    if manifest.get('state_version')!=state.get('state_version'): findings.append(finding('ERROR','STATE_VERSION_MISMATCH','manifest.state_version does not match canonical state_version'))
    state_req={x['id']:x for x in state.get('requirements',[]) if isinstance(x,dict) and x.get('id')}
    man_req={x['id']:x for x in manifest.get('requirements',[]) if isinstance(x,dict) and x.get('id')}
    for rid in man_req:
        if rid not in state_req: findings.append(finding('ERROR','REQ_NOT_CANONICAL',f'{rid} appears in manifest but not canonical state',rid))
    for rid,srec in state_req.items():
        if rid not in man_req: findings.append(finding('ERROR','REQ_MISSING_MANIFEST',f'{rid} missing from delivery manifest',rid)); continue
        m=man_req[rid]; ms=m.get('declared_status'); ss=srec.get('declared_status')
        compatible = (ms=='not_applicable' and ss in ('deferred','superseded')) or ms==ss or (ms=='satisfied' and ss=='satisfied')
        if not compatible: findings.append(finding('ERROR','REQ_STATE_DIVERGENCE',f'{rid}: manifest={ms}, canonical={ss}',rid))
        for ref in m.get('artifact_refs',[]) or []:
            if ref not in registry or registry[ref]['record_type']!='artifact': findings.append(finding('ERROR','REQ_ARTIFACT_REF',f'{rid} artifact_ref {ref} missing/wrong type',rid,ref))
        for ref in m.get('represents',[]) or []:
            if ref not in registry: findings.append(finding('ERROR','REQ_REPRESENTS_REF',f'{rid} represents unknown {ref}',rid,ref))
        for ref in m.get('verification_refs',[]) or []:
            if ref not in registry or registry[ref]['record_type']!='verification': findings.append(finding('ERROR','REQ_VER_REF',f'{rid} verification_ref {ref} missing/wrong type',rid,ref))
            elif registry[ref]['effective_status']!='passed': findings.append(finding('ERROR','REQ_VER_NOT_PASSED',f'{rid} verification {ref} is {registry[ref]["effective_status"]}',rid,ref))
    state_acc={x['id']:x for x in state.get('acceptance_criteria',[]) if isinstance(x,dict) and x.get('id')}
    man_acc={x['id']:x for x in manifest.get('acceptance_criteria',[]) if isinstance(x,dict) and x.get('id')}
    for aid in man_acc:
        if aid not in state_acc: findings.append(finding('ERROR','ACC_NOT_CANONICAL',f'{aid} appears in manifest but not canonical state',aid))
    for aid,srec in state_acc.items():
        if aid not in man_acc: findings.append(finding('ERROR','ACC_MISSING_MANIFEST',f'{aid} missing from delivery manifest',aid)); continue
        ms=man_acc[aid].get('declared_status'); ss=srec.get('declared_status')
        if ms!=ss: findings.append(finding('ERROR','ACC_STATE_DIVERGENCE',f'{aid}: manifest={ms}, canonical={ss}',aid))
        for ref in man_acc[aid].get('verification_refs',[]) or []:
            if ref not in registry or registry[ref]['record_type']!='verification': findings.append(finding('ERROR','ACC_VER_REF',f'{aid} verification_ref {ref} missing/wrong type',aid,ref))
            elif registry[ref]['effective_status']!='passed': findings.append(finding('ERROR','ACC_VER_NOT_PASSED',f'{aid} verification {ref} is {registry[ref]["effective_status"]}',aid,ref))
    state_art={x['id']:x for x in state.get('artifacts',[]) if isinstance(x,dict) and x.get('id')}
    delivered={x.get('id') for x in manifest.get('artifacts',[])}
    for aid,rec in state_art.items():
        if rec.get('materiality')=='material' and rec.get('declared_status') not in ('historical','superseded') and aid not in delivered:
            findings.append(finding('ERROR','ART_MISSING_MANIFEST',f'{aid} material artifact is absent from delivery manifest',aid))
    for m in manifest.get('artifacts',[]) or []:
        aid=m.get('id'); s=state_art.get(aid)
        if not s: findings.append(finding('ERROR','ART_STATE_MISSING',f'manifest artifact {aid} absent from canonical state',aid)); continue
        eff=registry.get(aid,{}).get('effective_status')
        if m.get('declared_current') and eff!='current': findings.append(finding('ERROR','ART_NOT_CURRENT',f'{aid} declared current in manifest but effective status is {eff}',aid))
        for ref in m.get('represents',[]) or []:
            if ref not in registry: findings.append(finding('ERROR','ART_REPRESENTS_REF',f'{aid} represents unknown {ref}',aid,ref))
        for ref in m.get('verification_refs',[]) or []:
            if ref not in registry or registry[ref]['record_type']!='verification': findings.append(finding('ERROR','ART_VER_REF',f'{aid} verification_ref {ref} missing/wrong type',aid,ref))
            elif registry[ref]['effective_status']!='passed': findings.append(finding('ERROR','ART_VER_NOT_PASSED',f'{aid} verification {ref} is {registry[ref]["effective_status"]}',aid,ref))
        if root and m.get('declared_current') and m.get('path'):
            p=(Path(root)/m['path']).resolve(); rr=Path(root).resolve()
            try: p.relative_to(rr)
            except ValueError: findings.append(finding('ERROR','ART_PATH_ESCAPE',f'{aid} path escapes root',aid))
            else:
                if not p.exists(): findings.append(finding('ERROR','ART_FILE_MISSING',f'{aid} current artifact file missing: {m["path"]}',aid))
    computed_ready=not any(f.severity=='ERROR' for f in findings) and not manifest.get('blocking_items') and not manifest.get('inconsistencies')
    if manifest.get('declared_delivery_ready') and not computed_ready: findings.append(finding('ERROR','DECLARED_READY_FALSE','declared_delivery_ready=true but computed_delivery_ready=false'))
    return findings, {'computed_delivery_ready':computed_ready,'epistemic_closure':closure}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('state_json'); ap.add_argument('delivery_manifest'); ap.add_argument('--root'); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
    try: s=load_json(Path(a.state_json)); m=load_json(Path(a.delivery_manifest))
    except Exception as e: print('ERROR:',e); return 1
    fs,comp=validate(s,m,Path(a.root) if a.root else None)
    if a.json: print(json.dumps({'findings':[f.as_dict() for f in fs],**comp},indent=2))
    else:
        for f in fs: print(f'{f.severity} [{f.code}] {f.message}')
        print('computed_delivery_ready:',comp['computed_delivery_ready'])
    return 1 if any(f.severity=='ERROR' for f in fs) else 0
if __name__=='__main__': raise SystemExit(main())
