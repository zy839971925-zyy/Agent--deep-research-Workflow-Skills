#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse, json
from runtime_core import (load_json, validate_plan, validate_schedule, validate_checkpoint,
                          validate_node_ledger, validate_capability_snapshot, evaluate_capabilities,
                          validate_worker_proposal)

def main():
    ap=argparse.ArgumentParser(description='Validate Reasoning Workflow execution-control artifacts')
    ap.add_argument('--plan',required=True)
    ap.add_argument('--schedule')
    ap.add_argument('--ledger')
    ap.add_argument('--capabilities')
    ap.add_argument('--worker-proposal')
    ap.add_argument('--checkpoint')
    ap.add_argument('--json',action='store_true')
    a=ap.parse_args(); root=Path(__file__).resolve().parents[1]
    plan=load_json(Path(a.plan)); findings=validate_plan(plan,root)
    ledger=load_json(Path(a.ledger)) if a.ledger else None
    schedule=load_json(Path(a.schedule)) if a.schedule else None
    if ledger: findings += validate_node_ledger(plan,ledger,root)
    if schedule: findings += validate_schedule(plan,schedule,root,ledger)
    if a.capabilities:
        snap=load_json(Path(a.capabilities)); findings += validate_capability_snapshot(snap,root); fs,_=evaluate_capabilities(plan,snap); findings += fs
    if a.worker_proposal:
        prop=load_json(Path(a.worker_proposal)); current_state_version=(ledger or {}).get('state_version'); findings += validate_worker_proposal(plan,prop,root,current_state_version)
    if a.checkpoint:
        findings += validate_checkpoint(load_json(Path(a.checkpoint)),root,plan,schedule)
    if a.json: print(json.dumps({'findings':[f.as_dict() for f in findings]},indent=2))
    else:
        for f in findings: print(f'{f.severity} [{f.code}] {f.message}')
    return 1 if any(f.severity=='ERROR' for f in findings) else 0
if __name__=='__main__': raise SystemExit(main())
