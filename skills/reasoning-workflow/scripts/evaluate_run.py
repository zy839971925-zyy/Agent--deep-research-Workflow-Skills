#!/usr/bin/env python3
"""Evaluate observable run artifacts only. Never stores or requires hidden chain-of-thought."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def matches(expected, actual):
    if isinstance(expected,str): return (actual.get('event') if isinstance(actual,dict) else actual)==expected
    if not isinstance(expected,dict) or not isinstance(actual,dict): return expected==actual
    for k,v in expected.items():
        if k.endswith('_any_of'):
            key=k[:-7]
            if actual.get(key) not in v: return False
        elif actual.get(k)!=v: return False
    return True

def validate(case,run):
    findings=[]; obs=case.get('observables',{}); events=run.get('events',[])
    for e in obs.get('expected_events',[]):
        if not any(matches(e,a) for a in events): findings.append({'severity':'ERROR','code':'MISSING_EVENT','message':f'missing expected event {e}'})
    for e in obs.get('forbidden_events',[]):
        if any(matches(e,a) for a in events): findings.append({'severity':'ERROR','code':'FORBIDDEN_EVENT','message':f'forbidden event occurred: {e}'})
    fs=run.get('final_state',{})
    for k,v in obs.get('expected_final_state',{}).items():
        if fs.get(k)!=v: findings.append({'severity':'ERROR','code':'FINAL_STATE','message':f'final_state.{k}={fs.get(k)!r}, expected {v!r}'})
    codes={x.get('code') for x in run.get('findings',[]) if isinstance(x,dict)}
    for c in obs.get('expected_findings',[]):
        if c not in codes: findings.append({'severity':'ERROR','code':'MISSING_FINDING','message':f'missing expected finding {c}'})

    # Adherence checks operate on observable events and state only. They never
    # inspect or require private chain-of-thought.
    profile=run.get('task_profile') or case.get('task_profile') or {}
    initial=run.get('initial_state') or {}
    route=run.get('route') or {}
    has_model=bool(initial.get('current_problem_model_ref')) or any(
        e.get('event') in ('problem_model_created','model_updated') and e.get('problem_model_ref')
        for e in events if isinstance(e,dict)
    )
    has_need=bool(initial.get('current_evidence_need_ref')) or any(
        e.get('event')=='evidence_need_created' and e.get('evidence_need_ref')
        for e in events if isinstance(e,dict)
    )
    for e in events:
        if not isinstance(e,dict): continue
        kind=e.get('event')
        if kind=='orientation_retrieval' and not e.get('orientation_goal'):
            findings.append({'severity':'ERROR','code':'ORIENTATION_WITHOUT_GOAL','message':'orientation retrieval requires an explicit orientation goal'})
        if kind=='evidence_retrieval':
            if not (e.get('evidence_need_ref') or has_need):
                findings.append({'severity':'ERROR','code':'EVIDENCE_RETRIEVAL_WITHOUT_NEED','message':'formal evidence retrieval requires a current evidence need'})
            if not (e.get('problem_model_ref') or has_model):
                findings.append({'severity':'ERROR','code':'EVIDENCE_NEED_WITHOUT_MODEL','message':'formal evidence retrieval requires a current problem model'})
        if kind=='reference_loaded' and e.get('family') not in route.get('required_families',[]):
            findings.append({'severity':'ERROR','code':'UNROUTED_FAMILY_REFERENCE','message':'reference loaded from a family outside the selected route'})
        if kind=='skill_default_overrode_user_instruction' and not e.get('hard_safety_or_authorization'):
            findings.append({'severity':'ERROR','code':'SKILL_OVERRIDE_USER','message':'skill defaults cannot override explicit user instructions'})
    deep_route=(profile.get('evidence_depth') in ('deep','max') or profile.get('depth_class') in ('deep','max') or profile.get('deep_research'))
    if deep_route and any(isinstance(e,dict) and e.get('event')=='retrieval_started' for e in events) and not any(isinstance(e,dict) and e.get('event')=='evidence_retrieval' for e in events):
        findings.append({'severity':'ERROR','code':'MISSING_OBLIGATION','message':'research route started without a formal evidence-retrieval obligation'})
    return findings

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('case'); ap.add_argument('run'); a=ap.parse_args(); case=json.loads(Path(a.case).read_text()); run=json.loads(Path(a.run).read_text()); fs=validate(case,run); print(json.dumps({'findings':fs,'passed':not fs},indent=2)); return 1 if fs else 0
if __name__=='__main__': raise SystemExit(main())
