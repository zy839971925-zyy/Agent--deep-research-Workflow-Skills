#!/usr/bin/env python3
from pathlib import Path
import argparse,json
try: import jsonschema
except ImportError: jsonschema=None

def validate(data,root):
    fs=[]
    if jsonschema is None:return [{'severity':'ERROR','code':'JSONSCHEMA_MISSING'}]
    schema=json.loads((root/'schemas'/'dual-verification.schema.json').read_text())
    for e in jsonschema.Draft202012Validator(schema).iter_errors(data): fs.append({'severity':'ERROR','code':'SCHEMA','message':e.message})
    if fs: return fs
    if data.get('reconciliation_status')=='reconciled' and not data.get('reconciliation_refs'):
        fs.append({'severity':'ERROR','code':'RECONCILIATION_EVIDENCE_REQUIRED','message':'reconciled review requires targeted verification/evidence references'})
    mode=data.get('mode'); l2=data.get('layer2')
    if mode in ('dual','dual_orthogonal') and not l2: fs.append({'severity':'ERROR','code':'SECOND_LAYER_REQUIRED','message':'dual verification requires layer2'})
    if l2:
        if l2.get('reviewer_context_id')==data.get('solver_context_id'): fs.append({'severity':'ERROR','code':'REVIEW_NOT_FRESH','message':'layer2 reviewer must not reuse solver context'})
        if l2.get('solver_transcript_included'): fs.append({'severity':'ERROR','code':'SOLVER_TRANSCRIPT_CONTAMINATION','message':'layer2 review should not receive full solver reasoning transcript'})
        basis=set(l2.get('independence_basis',[]))
        if mode=='dual_orthogonal' and not (basis & {'different_model','orthogonal_tool','orthogonal_evidence','human','deterministic_checker'}): fs.append({'severity':'ERROR','code':'ORTHOGONAL_BASIS_REQUIRED','message':'dual_orthogonal requires more than fresh context'})
        if mode=='dual_orthogonal' and l2.get('route_signature') and l2.get('route_signature')==l2.get('solver_route_signature') and not (basis & {'different_model','orthogonal_tool','orthogonal_evidence','human','deterministic_checker'}): fs.append({'severity':'ERROR','code':'CORRELATED_REVIEW_ROUTE','message':'identical review route cannot claim orthogonal independence'})
        if l2.get('verdict')=='conflict' and data.get('reconciliation_status') not in ('reopened','targeted_evidence_needed','reconciled','blocked'): fs.append({'severity':'ERROR','code':'REVIEW_CONFLICT_UNRESOLVED','message':'review conflict must reopen/reconcile, never majority-vote close'})
    return fs

def main():
    ap=argparse.ArgumentParser();ap.add_argument('record');ap.add_argument('--root',default='.');a=ap.parse_args();d=json.loads(Path(a.record).read_text());fs=validate(d,Path(a.root));print(json.dumps({'passed':not fs,'findings':fs},indent=2));return 1 if fs else 0
if __name__=='__main__':raise SystemExit(main())
