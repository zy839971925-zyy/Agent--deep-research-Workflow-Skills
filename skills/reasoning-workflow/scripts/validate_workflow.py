#!/usr/bin/env python3
"""Opt-in strict bridge for recorded, substantial work; no executor/authority claims."""
from pathlib import Path
import argparse,json,hashlib
from routing_core import validate_profile,route_task,recheck_profile
from validate_delivery import validate as delivery
from validate_dual_verification import validate as review_valid,verification_passed
from runtime_core import validate_schema
ROOT=Path(__file__).resolve().parents[1]

def fingerprint(state,refs):
    from reference_core import dependency_closure
    found=dependency_closure(state,refs)
    blob=json.dumps(found,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
    return 'sha256:'+hashlib.sha256(blob).hexdigest()

def validate_bridge(profile,route,state,manifest,bundle,root,review_verifier=None):
    """Mechanical bridge. Optional review_verifier is trusted HOST CODE, never JSON.

    Its receipt must bind this review/fingerprint and both layer refs. It must
    authenticate evidence/actual methods and assess orthogonality outside this
    package. No callback means no authenticated/orthogonal credit.
    """
    errors=[]; credit_errors=[]; authenticated=[]; orthogonal_credit=[]
    errors += validate_profile(profile,ROOT)
    if errors: return {'passed':False,'structural_valid':False,'computed_delivery_ready':False,'evidence_authenticated':False,'orthogonality_verified':None,'errors':errors,'host_execution_verified':False}
    if recheck_profile(profile,[])!=profile:
        return {'passed':False,'structural_valid':False,'computed_delivery_ready':False,'evidence_authenticated':False,'orthogonality_verified':None,'errors':['PROFILE_RECHECK_REQUIRED: normalize explicit depth and use the resulting profile/version and route'],'host_execution_verified':False}
    expected=route_task(profile)
    if route!=expected: errors.append('route differs from deterministic current profile requirements')
    fs,computed=delivery(state,manifest,root)
    errors += [f.code+': '+f.message for f in fs if f.severity=='ERROR']
    schema_errors=validate_schema(bundle,ROOT/'schemas/review-bundle.schema.json')
    errors += [f.code+': '+f.message for f in schema_errors]
    if schema_errors: return {'passed':False,'structural_valid':False,'computed_delivery_ready':False,'evidence_authenticated':False,'orthogonality_verified':None,'errors':errors,'host_execution_verified':False}
    if bundle['work_id']!=state.get('work_id'): errors.append('review bundle work identity mismatch')
    rank={'minimal':0,'single':1,'dual':2,'dual_orthogonal':3}
    canonical={v['id']:v for v in state.get('verification',[])}
    registry={row['id']:row for rows in state.values() if isinstance(rows,list) for row in rows if isinstance(row,dict) and 'id' in row}
    covered=set()
    for entry in bundle['reviews']:
        record=entry['record'];rid=record['verification_id'];vf=review_valid(record,ROOT)
        if vf: errors.append('invalid review '+rid);continue
        evidence_refs=list(record.get('layer1',{}).get('verification_refs',[])) + list((record.get('layer2') or {}).get('verification_refs',[])) + list(entry.get('independence_evidence_refs',[]))
        if any(ref not in registry or ref==rid or registry[ref].get('declared_status') not in ('current','passed','verified_complete') for ref in evidence_refs): errors.append('unresolved/stale review evidence '+rid);continue
        if not verification_passed(record): errors.append('review did not pass '+rid);continue
        if rank[record['mode']]<rank[expected['verification_mode']]: errors.append('insufficient review mode '+rid);continue
        try: actual=fingerprint(state,entry['target_refs'])
        except ValueError as e: errors.append(str(e));continue
        if actual!=entry['target_fingerprint']: errors.append('stale target fingerprint '+rid);continue
        c=canonical.get(rid)
        if not c or c.get('declared_status')!='passed' or set(c.get('target_refs',[]))!=set(entry['target_refs']): errors.append('canonical review binding mismatch '+rid);continue
        if c.get('metadata',{}).get('target_fingerprint')!=actual: errors.append('canonical fingerprint mismatch '+rid);continue
        # Claims about orthogonality require observable references, not just enum names.
        if record['mode']=='dual_orthogonal' and not entry.get('independence_evidence_refs'): errors.append('unsubstantiated orthogonality '+rid);continue
        if any(ref not in registry for ref in entry.get('independence_evidence_refs',[])): errors.append('unresolved independence evidence '+rid);continue
        if entry.get('context_exposure')!='packet_only' and 'fresh_context' in (record.get('layer2') or {}).get('independence_basis',[]): errors.append('fresh-context credit unsupported '+rid);continue
        authenticated.append(False)
        if record['mode']=='dual_orthogonal':
            l1=record['layer1'].get('verification_refs',[]);l2=record['layer2'].get('verification_refs',[])
            # Input evidence is not itself an executed layer verification.
            layer_bound=bool(l1 and l2 and set(l1).isdisjoint(l2))
            for ref in l1+l2:
                witness=canonical.get(ref,{})
                if (ref==rid or witness.get('declared_status')!='passed' or
                    not set(entry['target_refs'])<=set(witness.get('target_refs',[])) or
                    witness.get('metadata',{}).get('target_fingerprint')!=actual):layer_bound=False
            try: receipt=review_verifier(entry,state) if callable(review_verifier) else None
            except Exception: receipt=None
            receipt_bound=(isinstance(receipt,dict) and receipt.get('verification_id')==rid and
                receipt.get('target_fingerprint')==actual and receipt.get('layer1_verification_refs')==l1 and
                receipt.get('layer2_verification_refs')==l2)
            evidence_ok=bool(layer_bound and receipt_bound and receipt.get('evidence_authenticated') is True)
            orthogonal_ok=bool(evidence_ok and receipt.get('orthogonality_verified') is True)
            authenticated[-1]=evidence_ok;orthogonal_credit.append(orthogonal_ok)
            if not orthogonal_ok:credit_errors.append('ORTHOGONALITY_UNVERIFIED: trusted host evidence/method receipt and two bound layer verifications required '+rid)
        covered.update(entry['target_refs'])
    material={r['id'] for field in ('answers','artifacts','recommendations','decisions') for r in state.get(field,[]) if r.get('materiality')=='material' and r.get('declared_status') not in ('historical','superseded')}
    if not material: errors.append('strict bridge requires explicit material target scope')
    if material-covered: errors.append('unreviewed material targets: '+','.join(sorted(material-covered)))
    canonical_artifacts={row['id']:row for row in state.get('artifacts',[])}
    manifest_artifacts={row['id']:row for row in manifest.get('artifacts',[])}
    # Authoritative canonical status and obligations choose checks, never a worker flag.
    for c in canonical_artifacts.values():
        required_current=(c.get('declared_status')=='current' or (c.get('materiality')=='material' and c.get('declared_status') not in ('historical','superseded')))
        if not required_current:continue
        artifact=manifest_artifacts.get(c['id'])
        if not artifact or not artifact.get('declared_current'):
            errors.append('current/required artifact missing or downgraded '+c['id']);continue
        h=c.get('metadata',{}).get('content_sha256')
        try:
            if root is None: raise ValueError('artifact root required for strict file validation')
            rr=Path(root).resolve();path=(rr/artifact['path']).resolve();path.relative_to(rr)
            digest=hashlib.sha256(path.read_bytes()).hexdigest()
            if not h or h!=artifact.get('content_sha256') or digest!=h:errors.append('artifact digest mismatch/missing '+artifact['id'])
        except (ValueError,OSError,TypeError,KeyError):errors.append('artifact content unverified '+artifact['id'])
    passed=not errors and not credit_errors
    return {'passed':passed,'structural_valid':not errors,
        'computed_delivery_ready':passed and computed['computed_delivery_ready'],
        'evidence_authenticated':bool(authenticated) and all(authenticated),
        'orthogonality_verified':all(orthogonal_credit) if orthogonal_credit else None,
        'errors':errors+credit_errors,'host_execution_verified':False}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('profile','route','state','manifest','reviews'):p.add_argument('--'+n,required=True)
    p.add_argument('--root',type=Path,required=True);a=p.parse_args()
    try:
        args=[json.loads(Path(getattr(a,n)).read_text()) for n in ('profile','route','state','manifest','reviews')]
        result=validate_bridge(*args,a.root)
    except (ValueError,TypeError,KeyError,OSError) as e:result={'passed':False,'structural_valid':False,'computed_delivery_ready':False,'evidence_authenticated':False,'orthogonality_verified':None,'errors':[str(e)],'host_execution_verified':False}
    print(json.dumps(result,indent=2));return 0 if result['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
