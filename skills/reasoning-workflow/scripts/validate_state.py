#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from semantic_core import (load_json, validate_schema, build_registry, load_policy, typed_reference_findings,
                           cycle_findings, compute_effective, effective_state_findings, compute_epistemic_closure, compute_runtime_closure, summary, finding)

def validate(state: dict, root: Path | None = None):
    root=root or Path(__file__).resolve().parents[1]
    findings=validate_schema(state,root/'schemas/work-state.schema.json')
    registry,fs=build_registry(state); findings+=fs
    policy=load_policy(root)
    fs,edges=typed_reference_findings(registry,policy); findings+=fs
    findings+=cycle_findings(registry,edges,policy)
    compute_effective(registry,edges)
    findings+=effective_state_findings(registry)
    closure=compute_epistemic_closure(state,registry)
    runtime_closure=compute_runtime_closure(state,registry)
    if state.get('declared_status')=='closed' and state.get('lane') in ('question','mixed') and not closure['computed_epistemic_closed']:
        for b in closure['blockers']: findings.append(finding('ERROR','EPISTEMIC_CLOSURE_BLOCKED',b,state.get('root_question_ref') or ''))
    if state.get('declared_status')=='closed' and state.get('lane') in ('action','mixed') and not runtime_closure['computed_runtime_closed']:
        for b in runtime_closure['blockers']: findings.append(finding('ERROR','RUNTIME_CLOSURE_BLOCKED',b))
    # material effective stale items are blockers for declared delivery/closure
    if state.get('declared_status') in ('closed','delivery_ready'):
        for rid,node in registry.items():
            if node['record'].get('materiality','supporting')=='material' and node['effective_status'] in ('stale','invalidated','needs_recompute'):
                findings.append(finding('ERROR','MATERIAL_EFFECTIVE_STALE',f'{rid} is material and effectively {node["effective_status"]}',rid))
    return findings,registry,{"epistemic":closure,"runtime":runtime_closure}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('state_json'); ap.add_argument('--json',action='store_true'); args=ap.parse_args()
    root=Path(__file__).resolve().parents[1]
    try: state=load_json(Path(args.state_json))
    except Exception as e: print(f'ERROR: unable to read JSON: {e}'); return 1
    findings,reg,closure=validate(state,root)
    report={'findings':[f.as_dict() for f in findings],'effective_state':summary(reg),'closure':closure}
    if args.json: print(json.dumps(report,indent=2))
    else:
        for f in findings: print(f'{f.severity} [{f.code}] {f.message}')
        print('computed_epistemic_closed:',closure.get('epistemic',{}).get('computed_epistemic_closed'))
        print('computed_runtime_closed:',closure.get('runtime',{}).get('computed_runtime_closed'))
    return 1 if any(f.severity=='ERROR' for f in findings) else 0
if __name__=='__main__': raise SystemExit(main())
