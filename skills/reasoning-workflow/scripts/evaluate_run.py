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
    return findings

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('case'); ap.add_argument('run'); a=ap.parse_args(); case=json.loads(Path(a.case).read_text()); run=json.loads(Path(a.run).read_text()); fs=validate(case,run); print(json.dumps({'findings':fs,'passed':not fs},indent=2)); return 1 if fs else 0
if __name__=='__main__': raise SystemExit(main())
