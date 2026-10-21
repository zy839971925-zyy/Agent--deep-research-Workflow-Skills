#!/usr/bin/env python3
"""Schema + semantic admission is shared by validation and retrieval."""
from pathlib import Path
import argparse,json
from learning_core import retrieve,admit_record,file_evidence_resolver

def admit(records,root,resolver=None):
    if not isinstance(records,list): return [{'severity':'ERROR','code':'LEARNING_ENVELOPE'}]
    return [f for record in records for f in admit_record(record,root,resolver)]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('records');ap.add_argument('--task-tag',action='append',default=[]);ap.add_argument('--gap-tag',action='append',default=[]);ap.add_argument('--limit',type=int,default=3);ap.add_argument('--maintenance',action='store_true',help='Read advisory maintenance proposals; never authorizes application');ap.add_argument('--validation-evidence',type=Path);a=ap.parse_args()
    try:
        value=json.loads(Path(a.records).read_text())
        if isinstance(value,list): items=value
        elif isinstance(value,dict) and set(value)=={'learnings'} and isinstance(value['learnings'],list): items=value['learnings']
        else: raise ValueError('expected array or exactly {learnings: array}')
        resolver=file_evidence_resolver(a.validation_evidence)
        fs=admit(items,Path(__file__).resolve().parents[1],resolver)
    except (ValueError,OSError) as e: fs=[{'severity':'ERROR','code':'LEARNING_INPUT','message':str(e)}];items=[]
    print(json.dumps({'passed':not fs,'findings':fs,'advisory_only':a.maintenance,'selected':[] if fs else retrieve(items,a.task_tag,a.gap_tag,a.limit,a.maintenance,resolver)},indent=2));return 1 if fs else 0
if __name__=='__main__':raise SystemExit(main())
