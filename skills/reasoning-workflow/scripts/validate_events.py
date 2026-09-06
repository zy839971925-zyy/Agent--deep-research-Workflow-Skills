#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
from semantic_core import validate_schema, load_json, finding

def load_events(path):
    txt=Path(path).read_text(encoding='utf-8').strip()
    if not txt: return []
    if txt.lstrip().startswith('['): return json.loads(txt)
    return [json.loads(line) for line in txt.splitlines() if line.strip()]

def validate(events,state=None,root=None):
    root=root or Path(__file__).resolve().parents[1]; fs=[]; seen=set(); prev_seq=None; prev_to=None; wid=None
    ids=set()
    if state:
        for col,val in state.items():
            if isinstance(val,list):
                for x in val:
                    if isinstance(x,dict) and x.get('id'): ids.add(x['id'])
    for i,e in enumerate(events):
        fs+=validate_schema(e,root/'schemas/event.schema.json')
        eid=e.get('event_id')
        if eid in seen: fs.append(finding('ERROR','EVENT_DUP_ID',f'duplicate event_id {eid}',eid))
        seen.add(eid)
        if wid is None: wid=e.get('work_id')
        elif e.get('work_id')!=wid: fs.append(finding('ERROR','EVENT_WORK_ID',f'event {eid} has inconsistent work_id',eid))
        seq=e.get('event_seq'); fr=e.get('from_state_version'); to=e.get('to_state_version')
        if prev_seq is not None and seq!=prev_seq+1: fs.append(finding('ERROR','EVENT_SEQ_GAP',f'event_seq {prev_seq} -> {seq} is not contiguous',eid))
        if prev_to is not None and fr!=prev_to: fs.append(finding('ERROR','EVENT_VERSION_GAP',f'{eid} from_state_version {fr} != prior to_state_version {prev_to}',eid))
        if isinstance(fr,int) and isinstance(to,int) and to<=fr: fs.append(finding('ERROR','EVENT_VERSION_ORDER',f'{eid} to_state_version must exceed from_state_version',eid))
        for ref in (e.get('invalidates',[]) or [])+(e.get('supersedes',[]) or []):
            if state is not None and ref not in ids: fs.append(finding('ERROR','EVENT_REF',f'{eid} references unknown state id {ref}',eid,ref))
        prev_seq=seq; prev_to=to
    if state and events:
        if state.get('work_id')!=wid: fs.append(finding('ERROR','EVENT_STATE_WORK_ID','event ledger work_id differs from state'))
        if state.get('state_version')!=prev_to: fs.append(finding('ERROR','EVENT_STATE_VERSION',f'last event version {prev_to} != state_version {state.get("state_version")}'))
    return fs

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('events'); ap.add_argument('--state'); ap.add_argument('--json',action='store_true'); a=ap.parse_args()
    ev=load_events(a.events); st=load_json(Path(a.state)) if a.state else None; fs=validate(ev,st)
    if a.json: print(json.dumps({'findings':[f.as_dict() for f in fs]},indent=2))
    else:
        for f in fs: print(f'{f.severity} [{f.code}] {f.message}')
    return 1 if any(f.severity=='ERROR' for f in fs) else 0
if __name__=='__main__': raise SystemExit(main())
